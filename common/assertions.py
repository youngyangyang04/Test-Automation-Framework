import traceback
import allure
import jsonpath
import operator

from common.recordlog import logs
from common.connection import ConnectMysql


class Assertions:
    """"
    接口断言模式，支持
    1）响应文本字符串包含模式断言
    2）响应结果相等断言
    3）响应结果不相等断言
    4）响应结果任意值断言
    5）数据库断言

    """

    def contains_assert(self, value, response, status_code):
        """
        字符串包含断言模式，断言预期结果的字符串是否包含在接口的响应信息中
        :param value: 预期结果，yaml文件的预期结果值
        :param response: 接口实际响应结果
        :param status_code: 响应状态码
        :return: 返回结果的状态标识
        """
        # 断言状态标识，0成功，其他失败
        flag = 0
        for assert_key, assert_value in value.items():
            if assert_key == "status_code":
                if assert_value != status_code:
                    flag += 1
                    allure.attach(f"预期结果：{assert_value}\n实际结果：{status_code}", '响应代码断言结果:失败',
                                  attachment_type=allure.attachment_type.TEXT)
                    logs.error("contains断言失败：接口返回码【%s】不等于【%s】" % (status_code, assert_value))
            else:
                resp_list = jsonpath.jsonpath(response, "$..%s" % assert_key)
                if isinstance(resp_list[0], str):
                    resp_list = ''.join(resp_list)
                if resp_list:
                    assert_value = None if assert_value.upper() == 'NONE' else assert_value
                    if assert_value in resp_list:
                        logs.info("字符串包含断言成功：预期结果【%s】,实际结果【%s】" % (assert_value, resp_list))
                    else:
                        flag = flag + 1
                        allure.attach(f"预期结果：{assert_value}\n实际结果：{resp_list}", '响应文本断言结果：失败',
                                      attachment_type=allure.attachment_type.TEXT)
                        logs.error("响应文本断言失败：预期结果为【%s】,实际结果为【%s】" % (assert_value, resp_list))
        return flag

    def equal_assert(self, expected_results, actual_results, statuc_code=None):
        """
        相等断言模式
        :param expected_results: 预期结果，yaml文件validation值
        :param actual_results: 接口实际响应结果
        :return:
        """
        flag = 0
        if isinstance(actual_results, dict) and isinstance(expected_results, dict):
            # 找出实际结果与预期结果共同的key
            common_keys = list(expected_results.keys() & actual_results.keys())[0]
            # 根据相同的key去实际结果中获取，并重新生成一个实际结果的字典
            new_actual_results = {common_keys: actual_results[common_keys]}
            eq_assert = operator.eq(new_actual_results, expected_results)
            if eq_assert:
                logs.info(f"相等断言成功：接口实际结果：{new_actual_results}，等于预期结果：" + str(expected_results))
                allure.attach(f"预期结果：{str(expected_results)}\n实际结果：{new_actual_results}", '相等断言结果：成功',
                              attachment_type=allure.attachment_type.TEXT)
            else:
                flag += 1
                logs.error(f"相等断言失败：接口实际结果{new_actual_results}，不等于预期结果：" + str(expected_results))
                allure.attach(f"预期结果：{str(expected_results)}\n实际结果：{new_actual_results}", '相等断言结果：失败',
                              attachment_type=allure.attachment_type.TEXT)
        else:
            raise TypeError('相等断言--类型错误，预期结果和接口实际响应结果必须为字典类型！')
        return flag

    def not_equal_assert(self, expected_results, actual_results, statuc_code=None):
        """
        不相等断言模式
        :param expected_results: 预期结果，yaml文件validation值
        :param actual_results: 接口实际响应结果
        :return:
        """
        flag = 0
        if isinstance(actual_results, dict) and isinstance(expected_results, dict):
            # 找出实际结果与预期结果共同的key
            common_keys = list(expected_results.keys() & actual_results.keys())[0]
            # 根据相同的key去实际结果中获取，并重新生成一个实际结果的字典
            new_actual_results = {common_keys: actual_results[common_keys]}
            eq_assert = operator.ne(new_actual_results, expected_results)
            if eq_assert:
                logs.info(f"不相等断言成功：接口实际结果：{new_actual_results}，不等于预期结果：" + str(expected_results))
                allure.attach(f"预期结果：{str(expected_results)}\n实际结果：{new_actual_results}", '不相等断言结果：成功',
                              attachment_type=allure.attachment_type.TEXT)
            else:
                flag += 1
                logs.error(f"不相等断言失败：接口实际结果{new_actual_results}，等于预期结果：" + str(expected_results))
                allure.attach(f"预期结果：{str(expected_results)}\n实际结果：{new_actual_results}", '不相等断言结果：失败',
                              attachment_type=allure.attachment_type.TEXT)
        else:
            raise TypeError('不相等断言--类型错误，预期结果和接口实际响应结果必须为字典类型！')
        return flag

    def assert_response_any(self, actual_results, expected_results):
        """
        断言接口响应信息中的body的任何属性值
        :param actual_results: 接口实际响应信息
        :param expected_results: 预期结果，在接口返回值的任意值
        :return: 返回标识,0表示测试通过，非0则测试失败
        """
        flag = 0
        try:
            exp_key = list(expected_results.keys())[0]
            if exp_key in actual_results:
                act_value = actual_results[exp_key]
                rv_assert = operator.eq(act_value, list(expected_results.values())[0])
                if rv_assert:
                    logs.info("响应结果任意值断言成功")
                else:
                    flag += 1
                    logs.error("响应结果任意值断言失败")
        except Exception as e:
            logs.error(e)
            raise
        return flag

    def assert_response_time(self, res_time, exp_time):
        """
        通过断言接口的响应时间与期望时间对比,接口响应时间小于预期时间则为通过
        :param res_time: 接口的响应时间
        :param exp_time: 预期的响应时间
        :return:
        """
        try:
            assert res_time < exp_time
            return True
        except Exception as e:
            logs.error('接口响应时间[%ss]大于预期时间[%ss]' % (res_time, exp_time))
            raise

    def assert_mysql_data(self, expected_results):
        """
        数据库断言
        :param expected_results: 预期结果，yaml文件的SQL语句
        :return: 返回flag标识，0表示正常，非0表示测试不通过
        """
        flag = 0
        conn = ConnectMysql()
        db_value = conn.query_all(expected_results)
        if db_value is not None:
            logs.info("数据库断言成功")
        else:
            flag += 1
            logs.error("数据库断言失败，请检查数据库是否存在该数据！")
        return flag

    def assert_result(self, expected, response, status_code):
        """
        断言，通过断言all_flag标记，all_flag==0表示测试通过，否则为失败
        :param expected: 预期结果
        :param response: 实际响应结果
        :param status_code: 响应code码
        :return:
        """
        all_flag = 0
        try:
            logs.info("yaml文件预期结果：%s" % expected)
            # logs.info("实际结果：%s" % response)
            # all_flag = 0
            for yq in expected:
                for key, value in yq.items():
                    if key == "contains":
                        flag = self.contains_assert(value, response, status_code)
                        all_flag = all_flag + flag
                    elif key == "eq":
                        flag = self.equal_assert(value, response)
                        all_flag = all_flag + flag
                    elif key == 'ne':
                        flag = self.not_equal_assert(value, response)
                        all_flag = all_flag + flag
                    elif key == 'rv':
                        flag = self.assert_response_any(actual_results=response, expected_results=value)
                        all_flag = all_flag + flag
                    elif key == 'db':
                        flag = self.assert_mysql_data(value)
                        all_flag = all_flag + flag
                    else:
                        logs.error("不支持此种断言方式")

        except Exception as exceptions:
            logs.error('接口断言异常，请检查yaml预期结果值是否正确填写!')
            raise exceptions

        if all_flag == 0:
            logs.info("测试成功")
            assert True
        else:
            logs.error("测试失败")
            assert False
