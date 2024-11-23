import json
import re

import jenkins
from conf.operationConfig import OperationConfig


class PJenkins(object):
    conf = OperationConfig()

    def __init__(self):
        self.__config = {
            'url': self.conf.get_section_jenkins('url'),
            'username': self.conf.get_section_jenkins('username'),
            'password': self.conf.get_section_jenkins('password'),
            'timeout': int(self.conf.get_section_jenkins('timeout'))
        }
        self.__server = jenkins.Jenkins(**self.__config)

        self.job_name = self.conf.get_section_jenkins('job_name')

    def get_job_number(self):
        """读取jenkins job构建号"""
        build_number = self.__server.get_job_info(self.job_name).get('lastBuild').get('number')
        return build_number

    def get_build_job_status(self):
        """读取构建完成的状态"""
        build_num = self.get_job_number()
        job_status = self.__server.get_build_info(self.job_name, build_num).get('result')
        return job_status

    def get_console_log(self):
        """获取控制台日志"""
        console_log = self.__server.get_build_console_output(self.job_name, self.get_job_number())
        return console_log

    def get_job_description(self):
        """返回job描述信息"""
        description = self.__server.get_job_info(self.job_name).get('description')
        url = self.__server.get_job_info(self.job_name).get('url')

        return description, url

    def get_build_report(self):
        """返回第n次构建的测试报告"""
        report = self.__server.get_build_test_report(self.job_name, self.get_job_number())
        return report

    def report_success_or_fail(self):
        """统计测试报告用例成功数、失败数、跳过数以及成功率、失败率"""
        report_info = self.get_build_report()
        pass_count = report_info.get('passCount')
        fail_count = report_info.get('failCount')
        skip_count = report_info.get('skipCount')
        total_count = int(pass_count) + int(fail_count) + int(skip_count)
        duration = int(report_info.get('duration'))
        hour = duration // 3600
        minute = duration % 3600 // 60
        seconds = duration % 3600 % 60
        execute_duration = f'{hour}时{minute}分{seconds}秒'
        content = f'本次测试共执行{total_count}个测试用例，成功：{pass_count}个; 失败：{fail_count}个; 跳过：{skip_count}个; 执行时长：{hour}时{minute}分{seconds}秒'
        # 提取测试报告链接
        console_log = self.get_console_log()
        report_line = re.search(r'http://192.168.105.36:8088/job/hbjjapi/(.*?)allure', console_log).group(0)
        report_info = {
            'total': total_count,
            'pass_count': pass_count,
            'fail_count': fail_count,
            'skip_count': skip_count,
            'execute_duration': execute_duration,
            'report_line': report_line
        }
        return report_info


if __name__ == '__main__':
    p = PJenkins()
    res = p.report_success_or_fail()
    # result = re.search(r'http://192.168.105.36:8088/job/hbjjapi/(.*?)allure', res).group(0)
    print(res)
    # print(result)
