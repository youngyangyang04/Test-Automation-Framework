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
        file_path = 'extract.yaml'
        mode = 'w' if not os.path.exists(file_path) else 'a'
        self._write_yaml(file_path, data, mode)

    
if __name__ == '__main__':
    for testcase in get_testcase_yaml('login.yaml'):
        print(testcase)
        