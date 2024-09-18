import yaml
import os
def get_testcase_yaml(file):
    try:
        with open(file, 'r', encoding='utf-8') as f:
            for data in yaml.safe_load_all(f):
                yield data
    except Exception as e:
        print(f"Error reading YAML file: {e}")
        return


class ReadYamlData:
    def __init__(self, file=None):
        if file is None:
            self.file = 'login.yaml'
        else:
            self.file = file
    
    def _write_yaml(self, file_path, data, mode):
        with open(file_path, mode, encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True)
    
    def write_yaml_data(self, data):
        file_path = 'testcase/extract.yaml'
        mode = 'w' if not os.path.exists(file_path) else 'a'
        self._write_yaml(file_path, data, mode)

    def get_extract_yaml(self, node_name):
        """读取接口提取的变量值

        Args:
            node_name: extract.yaml文件中的key
        """
        if not os.path.exists('testcase/extract.yaml'):
            print('extract.yaml文件不存在')
            file = open('testcase/extract.yaml', 'w', encoding='utf-8')
            file.close()
            print('extract.yaml文件已创建')
            
        with open('testcase/extract.yaml', 'r', encoding='utf-8') as f:
            extract_data = yaml.safe_load(f)
            return extract_data[node_name]
    
if __name__ == '__main__':
    for testcase in get_testcase_yaml('login.yaml'):
        print(testcase)
        