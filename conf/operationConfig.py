import configparser
from conf.setting import FILE_PATH


class OperationConfig:
    """
    读取配置文件
    """

    def __init__(self, file_path=None):
        if file_path is None:
            self.file_path = FILE_PATH['conf']
        else:
            self.file_path = file_path
        self.config = configparser.ConfigParser()
        try:
            self.config.read(self.file_path, encoding='utf-8')
        except Exception as e:
            print(f"Error reading config file: {e}")

    def get_section_for_data(self, section, option):
        """
        获取配置文件中的数据
        :param section: ini 头部值
        :param option: 选项值的 key
        :return:
        """
        try:
            data = self.config.get(section, option)
            return data
        except Exception as e:
            print(f"Error reading config file: {e}")

    def get_envi(self, option):
        return self.get_section_for_data('api_envi', option)


if __name__ == '__main__':
    oper = OperationConfig()
    print(oper.get_envi('online_host'))
