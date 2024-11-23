import os
from common.recordlog import logs


def remove_file(filepath, endlst):
    """
    删除文件
    :param filepath: 路径
    :param endlst: 删除的后缀，例如：['json','txt','attach']
    :return:
    """
    try:
        if os.path.exists(filepath):
            # 获取该目录下所有文件名称
            dir_lst_files = os.listdir(filepath)
            for file_name in dir_lst_files:
                fpath = filepath + '\\' + file_name
                # endswith判断字符串是否以指定后缀结尾
                if isinstance(endlst, list):
                    for ft in endlst:
                        if file_name.endswith(ft):
                            os.remove(fpath)
                else:
                    raise TypeError('file Type error,must is list')
        else:
            os.makedirs(filepath)
    except Exception as e:
        logs.error(e)


def remove_directory(path):
    try:
        if os.path.exists(path):
            os.remove(path)
    except Exception as e:
        logs.error(e)
