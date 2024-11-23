import xml.etree.ElementTree as et
from conf.setting import FILE_PATH
from common.recordlog import logs


class OperXML:

    def read_xml(self, filename, tags, attr_value):
        """
        读取XML文件标签值
        :param filename: xml文件，只需要写文件名即可，传参不需要带路径
        :param tags: 读取哪个xml的标签
        :param attr_value: 标签中的属性，如id、name、class属性
        :return:
        """
        root = ''
        file_path = {
            'file': FILE_PATH['XML'] + '\\' + filename
        }
        try:
            tree = et.parse(file_path['file'])
            # 获取xml根标签
            root = tree.getroot()
        except Exception as e:
            logs.error(e)

        child_text = ''
        # 遍历整个xml文件
        for child in root.iter(tags):

            att = child.attrib

            if ''.join(list(att.values())) == attr_value:
                child_text = child.text.strip()
            if child:
                for i in child:
                    attr = i.attrib
                    if ''.join(list(attr.values())) == attr_value:
                        child_text = i.text.strip()

        return child_text

    def get_attribute_value(self, filename, tags):
        """
        读取标签属性值
        :param filename: 文件路径
        :param tags: xml标签名
        :return: dict格式
        """

        root = ''
        file_path = {'file': FILE_PATH['RESULTXML'] + '\\' + filename}
        try:
            tree = et.parse(file_path['file'])
            # 获取xml根标签
            root = tree.getroot()
        except Exception as e:
            logs.error(e)

        attr = [child.attrib for child in root.iter(tags)][0]

        return attr
