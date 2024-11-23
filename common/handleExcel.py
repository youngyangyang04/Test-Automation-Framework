import os

import xlrd
from conf import setting
from xlutils.copy import copy
from common.recordlog import logs
import xlwt


class OperationExcel(object):
    """
    封装读取/写入Excel文件的数据
    """

    def __init__(self, filename=None):
        try:
            if filename is not None:
                self.__filename = filename
            else:
                self.__filename = setting.FILE_PATH['EXCEL']
            self.__sheet_id = setting.SHEET_ID
        except Exception as e:
            logs.error(e)
        self.__GLOBAL_TABLE = self.xls_obj()
        self.colx = 0

    def xls_obj(self):
        xls_obj = ''
        if os.path.splitext(self.__filename)[-1] != '.xlsx':
            data = xlrd.open_workbook(self.__filename, formatting_info=True)
            xls_obj = data.sheets()[self.__sheet_id]
        else:
            logs.error('Excel文件的格式必须为.xls格式，请重新另存为xls格式！')
            exit()
        return xls_obj

    def get_rows(self):
        """
        获取xls文件总行数
        @return:
        """
        return self.__GLOBAL_TABLE.nrows

    def get_cols(self):
        """
        获取总列数
        :return:
        """
        return self.__GLOBAL_TABLE.ncols

    def get_cell_value(self, row, col):
        """
        获取单元格的值
        :param row: excel行数，索引从0开始，第一行索引是0
        :param col: Excel列数，索引从0开始，第一列索引是0
        :return:
        """
        return self.__GLOBAL_TABLE.cell_value(row, col)

    def settingStyle(self):
        """
        设置样式,该功能暂时未生效
        :return:
        """
        style = xlwt.easyfont("font:bold 1,color red")  # 粗体,红色

    def write_xls_value(self, row, col, value):
        """
        写入数据
        :param row: excel行数
        :param col: Excel列数
        :param value: 写入的值
        :return:
        """
        try:
            init_table = xlrd.open_workbook(self.__filename, formatting_info=True)
            copy_table = copy(init_table)
            sheet = copy_table.get_sheet(self.__filename)
            sheet.write(row, col, value)
            copy_table.save(self.__filename)
        except PermissionError:
            logs.error("请先关闭xls文件")
            exit()

    def get_each_line(self, row):
        """
        获取每一行数据
        :param row: excel行数
        :return: 返回一整行的数据
        """
        try:
            return self.__GLOBAL_TABLE.row_values(row)
        except Exception as exp:
            logs.error(exp)

    def get_each_column(self, col=None):
        """
        获取每一列数据
        :param col: Excel列数
        :return: 返回一整列的数据
        """
        if col is None:
            return self.__GLOBAL_TABLE.col_values(self.colx)
        else:
            return self.__GLOBAL_TABLE.col_values(col)
