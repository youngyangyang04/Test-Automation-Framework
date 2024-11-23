import sys
import traceback

# sys.path.insert(0, "..")

import configparser
from conf import setting
from common.recordlog import logs


class OperationConfig:
    """封装读取*.ini配置文件模块"""

    def __init__(self, filepath=None):

        if filepath is None:
            self.__filepath = setting.FILE_PATH['CONFIG']
        else:
            self.__filepath = filepath

        self.conf = configparser.ConfigParser()
        try:
            self.conf.read(self.__filepath, encoding='utf-8')
        except Exception as e:
            exc_type, exc_value, exc_obj = sys.exc_info()
            logs.error(str(traceback.print_exc(exc_obj)))

        self.type = self.get_report_type('type')

    def get_item_value(self, section_name):
        """
        :param section_name: 根据ini文件的头部值获取全部值
        :return:以字典形式返回
        """
        items = self.conf.items(section_name)
        return dict(items)

    def get_section_for_data(self, section, option):
        """
        :param section: ini文件头部值
        :param option:头部值下面的选项
        :return:
        """
        try:
            values = self.conf.get(section, option)
            return values
        except Exception as e:
            logs.error(str(traceback.format_exc()))
            return ''

    def write_config_data(self, section, option_key, option_value):
        """
        写入数据到ini配置文件中
        :param section: 头部值
        :param option_key: 选项值key
        :param option_value: 选项值value
        :return:
        """
        if section not in self.conf.sections():
            # 添加一个section值
            self.conf.add_section(section)
            self.conf.set(section, option_key, option_value)
        else:
            logs.info('"%s"值已存在，写入失败' % section)
        with open(self.__filepath, 'w', encoding='utf-8') as f:
            self.conf.write(f)

    def get_section_mysql(self, option):
        return self.get_section_for_data("MYSQL", option)

    def get_section_redis(self, option):
        return self.get_section_for_data("REDIS", option)

    def get_section_clickhouse(self, option):
        return self.get_section_for_data("CLICKHOUSE", option)

    def get_section_mongodb(self, option):
        return self.get_section_for_data("MongoDB", option)

    def get_report_type(self, option):
        return self.get_section_for_data('REPORT_TYPE', option)

    def get_section_ssh(self, option):
        return self.get_section_for_data("SSH", option)