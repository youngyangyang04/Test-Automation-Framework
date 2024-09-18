from common.read_yaml import ReadYamlData
import random as rd

class DebugTalk:
    def __init__(self):
        self.read = ReadYamlData()
    def get_extract_data(self, node_name, randoms=None):
        """
        根据指定的节点名称和随机选项从extract.yaml文件中提取数据。

        参数:
        - node_name: str，指定要读取数据的节点名称。
        - randoms: 可选[int]，决定如何处理extract.yaml文件中的数据。默认为None，表示不使用随机逻辑。

        返回:
        - 根据randoms的值，返回不同类型的数据处理结果。可能是一个随机选择的数据项，所有数据项的逗号分隔字符串，或者逗号分隔后的列表。

        说明:
        - 当randoms为0时，返回extract.yaml文件中随机选择的一个数据项。
        - 当randoms为-1时，返回所有数据项，使用逗号分隔。
        - 当randoms为-2时，返回所有数据项，先使用逗号分隔，再分割成列表。
        """
        data = self.read.get_extract_yaml(node_name)

        data_value = {
            0: rd.choice(data),  # 随机选择一个数据项
            -1: ','.join(data),  # 返回所有数据项，使用逗号分隔
            -2: ','.join(data).split(',')  # 返回所有数据项，先使用逗号分隔，再分割成列表
        }

        return data_value[int(randoms)]
    
    def md5_params(self, params):
        """对params进行md5加密

        Args:
            params: 需要加密的参数
        """
        pass
    

if __name__ == '__main__':
    debug = DebugTalk()
    print(debug.get_extract_data('product_id', randoms=-2))
    