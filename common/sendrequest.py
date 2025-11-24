import json
import allure
import pytest
import requests
import urllib3
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

from conf import setting
from common.recordlog import logs
from common.readyaml import ReadYamlData
from urllib3.exceptions import InsecureRequestWarning


class SendRequest:
    """轻量 HTTP 客户端，统一请求入口"""

    def __init__(
        self,
        cookie=None,
        session=None,
        default_timeout=None,
        retries=3,
        backoff_factor=0.2,
    ):
        self.cookie = cookie
        self.read = ReadYamlData()
        self.default_timeout = default_timeout or setting.API_TIMEOUT
        self.session = session or self._build_session(retries, backoff_factor)
        urllib3.disable_warnings(InsecureRequestWarning)

    @staticmethod
    def _build_session(retries, backoff_factor):
        session = requests.Session()
        if retries and retries > 0:
            retry_cfg = Retry(
                total=retries,
                connect=retries,
                read=retries,
                backoff_factor=backoff_factor,
                status_forcelist=[429, 502, 503, 504],
                allowed_methods=[
                    "HEAD",
                    "GET",
                    "OPTIONS",
                    "POST",
                    "PUT",
                    "PATCH",
                    "DELETE",
                ],
            )
            adapter = HTTPAdapter(max_retries=retry_cfg)
        else:
            adapter = HTTPAdapter()
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    @staticmethod
    def _mask_sensitive(headers):
        """隐藏敏感头字段，避免日志泄漏"""
        if not headers:
            return headers
        sensitive_keys = {"authorization", "token", "cookie", "set-cookie"}
        masked = {}
        for key, value in headers.items():
            if key.lower() in sensitive_keys:
                masked[key] = "***"
            else:
                masked[key] = value
        return masked

    def request(
        self,
        method,
        url,
        *,
        params=None,
        data=None,
        json=None,
        headers=None,
        cookies=None,
        files=None,
        timeout=None,
        **kwargs,
    ):
        """
        统一的请求入口，包装 requests.Session.request
        :return: Response 对象
        """
        method = method.upper() if method else "GET"
        timeout = timeout or self.default_timeout
        masked_headers = self._mask_sensitive(headers)
        try:
            logs.info(
                "请求 -> %s %s headers=%s params=%s data=%s json=%s",
                method,
                url,
                masked_headers,
                params,
                data,
                json,
            )
            result = self.session.request(
                method=method,
                url=url,
                params=params,
                data=data,
                json=json,
                headers=headers,
                cookies=cookies,
                files=files,
                timeout=timeout,
                verify=False,
                **kwargs,
            )
            set_cookie = requests.utils.dict_from_cookiejar(result.cookies)
            if set_cookie:
                self.read.write_yaml_data({"Cookie": set_cookie})
                logs.info("写入 Cookie：%s", set_cookie)
            logs.info("响应 <- %s %s status=%s", method, url, result.status_code)
            return result
        except requests.exceptions.ConnectionError:
            logs.error("ConnectionError--连接异常")
            pytest.fail(
                "接口请求异常，可能是request的连接数过多或请求速度过快导致程序报错！"
            )
        except requests.exceptions.HTTPError:
            logs.error("HTTPError--http异常")
            pytest.fail("HTTP 异常，请检查接口状态！")
        except requests.exceptions.RequestException as e:
            logs.error(e)
            pytest.fail("请求异常，请检查系统或数据是否正常！")

    def get(self, url, data=None, header=None):
        """向后兼容的 GET 包装"""
        response = self.request(
            "GET", url, params=data, headers=header, cookies=self.cookie
        )
        if response is None:
            return None
        return self._to_legacy_dict(response)

    def post(self, url, data=None, header=None):
        """向后兼容的 POST 包装"""
        response = self.request(
            "POST", url, data=data, headers=header, cookies=self.cookie
        )
        if response is None:
            return None
        return self._to_legacy_dict(response)

    @staticmethod
    def _to_legacy_dict(response):
        """兼容旧接口返回的结构"""
        res_ms = response.elapsed.microseconds / 1000
        res_second = response.elapsed.total_seconds()
        response_dict = {
            "code": response.status_code,
            "text": response.text,
            "res_ms": res_ms,
            "res_second": res_second,
        }
        try:
            response_dict["body"] = response.json().get("body")
        except Exception:
            response_dict["body"] = ""
        return response_dict

    def run_main(
        self, name, url, case_name, header, method, cookies=None, file=None, **kwargs
    ):
        """
        接口请求
        :param name: 接口名
        :param url: 接口地址
        :param case_name: 测试用例
        :param header:请求头
        :param method:请求方法
        :param cookies：默认为空
        :param file: 上传文件接口
        :param kwargs: 请求参数，根据yaml文件的参数类型
        :return:
        """

        try:
            # 收集报告日志
            logs.info("接口名称：%s" % name)
            logs.info("请求地址：%s" % url)
            logs.info("请求方式：%s" % method)
            logs.info("测试用例名称：%s" % case_name)
            logs.info("请求头：%s" % self._mask_sensitive(header))
            logs.info("Cookie：%s" % cookies)
            req_params = json.dumps(kwargs, ensure_ascii=False)
            if "data" in kwargs.keys():
                allure.attach(req_params, "请求参数", allure.attachment_type.TEXT)
                logs.info("请求参数：%s" % kwargs)
            elif "json" in kwargs.keys():
                allure.attach(req_params, "请求参数", allure.attachment_type.TEXT)
                logs.info("请求参数：%s" % kwargs)
            elif "params" in kwargs.keys():
                allure.attach(req_params, "请求参数", allure.attachment_type.TEXT)
                logs.info("请求参数：%s" % kwargs)
        except Exception as e:
            logs.error(e)
        response = self.request(
            method=method,
            url=url,
            headers=header,
            cookies=cookies,
            files=file,
            timeout=setting.API_TIMEOUT,
            **kwargs,
        )
        return response
