import datetime
import os
import cgitb
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
from PyQt5 import QtGui, QtWidgets
import json
import traceback
import yaml
import requests
from PyQt5 import QtCore
from hashlib import sha1
import base64
import urllib3

cgitb.enable(format='text')


class LogThread(QThread):
    # 设置线程变量
    trigger = pyqtSignal(str)

    def __int__(self, parent=None):
        super(LogThread, self).__init__(parent)

    def run_(self, message):
        """向信号trigger发送消息"""
        self.trigger.emit(message)


class NewTestCaseTools(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(NewTestCaseTools, self).__init__(parent)
        self.setupUI()

        # self.threads = LogThread(self)  # 自定义线程类
        # self.threads.trigger.connect(self.update_text)  # 当信号接收到消息时，更新数据
        # 初始化子窗口
        self.child_win = ToolMD5Window()
        self.child_win_base64 = ToolBase64Window()
        self.child_win_sha1 = ToolSha1Window()

    def setupUI(self):
        loadUi('./new_tools.ui', self)
        # 一些控件的设置可在此方法设置
        self.controls_setting()
        self.set_api_name()
        self.set_url()
        self.set_methods()
        self.set_requests_header()
        self.set_request_params()
        self.set_testcase_name()
        # self.set_assert_type()
        self.set_assert_params()
        self.set_depend_type()
        self.set_extract_data_type()
        self.set_depend_extract_params()
        # self.testcase_template()
        # self.create_testcase_directory()
        self.other_func()
        self.get_files()
        self.get_assert_params()
        self.radioButton.setChecked(True)
        self.radioButton_6.setChecked(True)
        self.get_depend_params()
        self.menu.setTitle("系统设置")
        self.menu_2.setTitle("编辑")
        self.menu_3.setTitle("帮助")
        self.actionhostpeizhi.setText("host设置")
        self.actionmorenqingqiutou.setText("默认请求头设置")
        self.actionbangzhuxinxi.setText("帮助信息")

    def closeEvent(self, event):
        """关闭窗口弹框"""
        reply = QtWidgets.QMessageBox.question(self, '警告', '退出后测试将停止,\n你确认要退出吗？',
                                               QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            # self.outputToFile()  # 关闭程序时自动保存控制台log
            event.accept()
        else:
            event.ignore()

    # def __reset_button(self):
    #     loadUi('./new_tools.ui', self)

    def bounced(self, text, title='提示'):
        """
        提示弹框
        :param text: 提示框内容
        :param title: 提示框标题，默认为”提示“
        :return:
        """

        try:
            quitMsgBox = QMessageBox()
            quitMsgBox.setWindowTitle(title)
            quitMsgBox.setText(text)
            # 设置自定义弹框大小
            # quitMsgBox.resize(400, 300)
            buttonY = QPushButton('确定')
            quitMsgBox.addButton(buttonY, QMessageBox.YesRole)
            quitMsgBox.exec_()
            buttonY.close()
        except Exception as e:
            print(e)

    def set_api_name(self):
        self.lineEdit.setClearButtonEnabled(True)

    def get_api_name(self):
        """获取接口名"""
        api_name = self.lineEdit.text().strip()
        if api_name == "":
            self.bounced("接口名不能为空")
        return api_name

    def set_url(self):
        self.lineEdit_2.setClearButtonEnabled(True)

    def get_url(self):
        """url"""
        url = self.lineEdit_2.text()
        if url == "":
            self.bounced("url不能为空")
        return url

    def set_methods(self):
        # 添加一个下拉选项
        method = ['GET', 'POST', 'PUT', 'DELETE']
        for m in method:
            self.comboBox.addItem(m)

    def get_method(self):
        """获取请求方法"""
        method = self.comboBox.currentText()
        return method

    def set_requests_header(self):
        # 设置表格宽度
        self.tableWidget.setColumnWidth(0, 120)
        self.tableWidget.setColumnWidth(1, 220)
        self.tableWidget.horizontalHeader().setStyleSheet(
            "color: rgb(0, 83, 128);border:1px solid rgb(210, 210, 210);")
        # 设置单元格高度
        self.tableWidget.setRowHeight(0, 50)
        self.tableWidget.setRowHeight(1, 50)
        self.pushButton.clicked.connect(lambda: self.add_table_row(self.tableWidget))
        self.pushButton_2.clicked.connect(lambda: self.delete_table_row(self.tableWidget))

    def get_header(self):
        tables_header_data = {}
        table_rows = self.tableWidget.rowCount()
        table_cols = self.tableWidget.columnCount()
        # 存储表格数据
        for i in range(0, table_rows):
            for j in range(0, table_cols):
                # 字典的列索引值固定
                tables_header_data[self.tableWidget.item(i, 0).text()] = self.tableWidget.item(i, j).text()
        if not tables_header_data:
            tables_header_data = ''

        return tables_header_data

    def add_table_row(self, table_widget):
        cur_count = table_widget.rowCount()
        cur_count += 1
        table_widget.setRowCount(cur_count)

    def delete_table_row(self, table_widget):
        row_items = table_widget.selectedItems()
        if row_items:
            # 求出所选择的行数
            selected_rows = []
            for i in row_items:
                row = i.row()
                if row not in selected_rows:
                    selected_rows.append(row)
            for r in range(len(sorted(selected_rows))):
                table_widget.removeRow(selected_rows[r] - r)  # 删除行

    def get_tables_data(self, table_widget):
        tables_data = {}
        table_rows = table_widget.rowCount()  # 获取表格行数
        table_cols = table_widget.columnCount()  # 获取表格列数
        # 存储表格数据
        for i in range(0, table_rows):
            for j in range(0, table_cols):
                # 字典的列索引值固定
                tables_data[table_widget.item(i, 0).text()] = table_widget.item(i, j).text()

        return tables_data

    def set_testcase_name(self):
        self.lineEdit_3.setClearButtonEnabled(True)

    def case_name(self):
        case_name = self.lineEdit_3.text().strip()
        if case_name == "":
            self.bounced("用例名不能为空")
        return case_name

    def set_request_params(self):
        # 设置tab标签页名，根据索引设置，从0起始
        self.tabWidget.setTabText(0, 'params')
        self.tabWidget.setTabText(1, 'form-data')
        self.tabWidget.setTabText(2, 'json')
        self.tabWidget.setTabText(3, 'files')
        # 设置tab页1--params
        self.tableWidget_2.setColumnWidth(0, 120)
        self.tableWidget_2.setColumnWidth(1, 220)
        self.tabWidget.setCurrentIndex(0)
        # 表格表头设置外框线
        self.tableWidget_2.horizontalHeader().setStyleSheet(
            "color: rgb(0, 83, 128);border:1px solid rgb(210, 210, 210);")
        # 设置单元格高度
        self.tableWidget_2.setRowHeight(0, 50)
        self.tableWidget_2.setRowHeight(1, 50)
        self.pushButton_4.clicked.connect(lambda: self.add_table_row(self.tableWidget_2))
        self.pushButton_5.clicked.connect(lambda: self.delete_table_row(self.tableWidget_2))
        # 设置tab页2--from-data
        self.tableWidget_3.setColumnWidth(0, 120)
        self.tableWidget_3.setColumnWidth(1, 220)
        self.tableWidget_3.horizontalHeader().setStyleSheet(
            "color: rgb(0, 83, 128);border:1px solid rgb(210, 210, 210);")
        # 设置单元格高度
        self.tableWidget_3.setRowHeight(0, 50)
        self.tableWidget_3.setRowHeight(1, 50)
        self.pushButton_6.clicked.connect(lambda: self.add_table_row(self.tableWidget_3))
        self.pushButton_7.clicked.connect(lambda: self.delete_table_row(self.tableWidget_3))
        # 设置tab页3--json
        self.textEdit.setAcceptRichText(False)
        # 设置tab页4--files
        self.tableWidget_4.setColumnWidth(0, 120)
        self.tableWidget_4.setColumnWidth(1, 220)
        self.tableWidget_4.horizontalHeader().setStyleSheet(
            "color: rgb(0, 83, 128);border:1px solid rgb(210, 210, 210);")
        self.lineEdit_9.setPlaceholderText('参数名')
        self.lineEdit_9.setClearButtonEnabled(True)
        self.lineEdit_10.setPlaceholderText('文件路径')
        self.lineEdit_10.setClearButtonEnabled(True)
        # 设置单元格高度
        self.tableWidget_4.setRowHeight(0, 50)
        self.tableWidget_4.setRowHeight(1, 50)
        self.pushButton_8.clicked.connect(lambda: self.add_table_row(self.tableWidget_4))
        self.pushButton_9.clicked.connect(lambda: self.delete_table_row(self.tableWidget_4))
        self.pushButton_3.clicked.connect(self.open_file)

    def request_params(self):
        params_type = self.tabWidget.tabText(self.tabWidget.currentIndex())
        tables_request_data = {}
        if params_type == 'params':
            table_rows = self.tableWidget_2.rowCount()
            table_cols = self.tableWidget_2.columnCount()
            # 存储表格数据
            for i in range(0, table_rows):
                for j in range(0, table_cols):
                    if self.tableWidget_2.item(i, j) is None:
                        tables_request_data[self.tableWidget_2.item(i, 0).text()] = ''
                    else:
                        tables_request_data[self.tableWidget_2.item(i, 0).text()] = self.tableWidget_2.item(i, j).text()

        elif params_type == 'form-data':
            params_type = 'data'
            table_rows = self.tableWidget_3.rowCount()
            table_cols = self.tableWidget_3.columnCount()
            for i in range(0, table_rows):
                for j in range(0, table_cols):
                    if self.tableWidget_3.item(i, j) is None:
                        tables_request_data[self.tableWidget_3.item(i, 0).text()] = ''
                    else:
                        tables_request_data[self.tableWidget_3.item(i, 0).text()] = self.tableWidget_3.item(i, j).text()
        elif params_type == 'json':
            text = self.textEdit.toPlainText()
            if text:
                tables_request_data = json.loads(text)

        elif params_type == 'files':
            table_rows = self.tableWidget_4.rowCount()
            table_cols = self.tableWidget_4.columnCount()
            for i in range(0, table_rows):
                for j in range(0, table_cols):
                    # 表格设置值
                    # self.tableWidget_4.setItem(i, 1, QTableWidgetItem(file_name[0]))
                    tables_request_data[self.tableWidget_4.item(i, 0).text()] = self.tableWidget_4.item(i, j).text()
            file_param = self.lineEdit_9.text()
            file_name = self.lineEdit_10.text()

            if file_name != '':
                tables_request_data = {file_param: file_name}
            else:
                return tables_request_data
        if not tables_request_data:
            tables_request_data = ''

        return params_type, tables_request_data

    def tab_click(self):
        """tab标签点击事件"""
        # self.tabWidget.currentChanged.connect(self.request_params)

    def get_files(self):
        files_dict = {}
        table_rows = self.tableWidget_4.rowCount()
        table_cols = self.tableWidget_4.columnCount()
        for i in range(0, table_rows):
            for j in range(0, table_cols):
                files_dict[self.tableWidget_4.item(i, 0).text()] = self.tableWidget_4.item(i, j).text()

        return files_dict

    def set_assert_type(self):
        """断言类型，返回id属性"""
        # 设置单选默认选项

    def set_assert_params(self):
        self.tableWidget_5.setColumnWidth(0, 120)
        self.tableWidget_5.setColumnWidth(1, 220)
        # 设置单元格高度
        self.tableWidget_5.setRowHeight(0, 50)
        self.tableWidget_5.setRowHeight(1, 50)
        self.tableWidget_5.horizontalHeader().setStyleSheet(
            "color: rgb(0, 83, 128);border:1px solid rgb(210, 210, 210);")
        self.pushButton_11.clicked.connect(lambda: self.add_table_row(self.tableWidget_5))
        self.pushButton_10.clicked.connect(lambda: self.delete_table_row(self.tableWidget_5))

    def get_assert_params(self):
        assert_list = []
        assert_type = None
        # 新建组
        self.radioButtonGroup_1 = QtWidgets.QButtonGroup(self.groupBox_2)
        # 将第一组单选按钮加入到分组中,并设置按钮id
        self.radioButtonGroup_1.addButton(self.radioButton, 1001)
        self.radioButtonGroup_1.addButton(self.radioButton_2, 1002)
        assert_id = self.radioButtonGroup_1.checkedId()

        if assert_id == 1001:
            assert_type = "contains"
        elif assert_id == 1002:
            assert_type = "equal"

        tables_data = {}
        table_rows = self.tableWidget_5.rowCount()  # 获取表格行数
        table_cols = self.tableWidget_5.columnCount()  # 获取表格列数
        # 存储表格数据
        for i in range(0, table_rows):
            for j in range(0, table_cols):
                # 字典的列索引值固定
                tables_data[self.tableWidget_5.item(i, 0).text()] = self.tableWidget_5.item(i, j).text()

        for key, value in tables_data.items():
            assert_list.append({assert_type: {key: value}})

        if not assert_list:
            assert_list = ''

        return assert_list

    def set_depend_type(self):
        # 设置单选按钮默认选中项
        self.radioButton_4.setChecked(True)

    def set_extract_data_type(self):
        self.radioButtonGroup_3 = QtWidgets.QButtonGroup(self.groupBox_2)
        # 将第一组单选按钮加入到分组中,并设置按钮id
        self.radioButtonGroup_3.addButton(self.radioButton_3, 1003)
        self.radioButtonGroup_3.addButton(self.radioButton_4, 1004)

    def set_depend_extract_params(self):
        self.tableWidget_6.setColumnWidth(0, 120)
        self.tableWidget_6.setColumnWidth(1, 220)
        self.tableWidget_6.horizontalHeader().setStyleSheet(
            "color: rgb(0, 83, 128);border:1px solid rgb(210, 210, 210);")
        # 设置单元格高度
        self.tableWidget_6.setRowHeight(0, 50)
        self.tableWidget_6.setRowHeight(1, 50)
        self.pushButton_13.clicked.connect(lambda: self.add_table_row(self.tableWidget_6))
        self.pushButton_12.clicked.connect(lambda: self.delete_table_row(self.tableWidget_6))

    def get_depend_params(self):
        extract_dict = {}
        self.radioButtonGroup_2 = QtWidgets.QButtonGroup(self.groupBox_2)
        # 将第一组单选按钮加入到分组中,并设置按钮id
        self.radioButtonGroup_2.addButton(self.radioButton_6, 1005)
        self.radioButtonGroup_2.addButton(self.radioButton_5, 1006)

        extract_type_id = self.radioButtonGroup_2.checkedId()

        tables_data = {}
        table_rows = self.tableWidget_6.rowCount()  # 获取表格行数
        table_cols = self.tableWidget_6.columnCount()  # 获取表格列数
        for i in range(0, table_rows):
            for j in range(0, table_cols):
                # 字典的列索引值固定
                tables_data[self.tableWidget_6.item(i, 0).text()] = self.tableWidget_6.item(i, j).text()

        if extract_type_id == 1005:
            extract_dict = {
                'extract': tables_data
            }
        elif extract_type_id == 1006:
            extract_dict = {
                'extract_list': tables_data
            }

        return extract_dict

    def controls_setting(self):
        self.lineEdit_6.setClearButtonEnabled(True)
        self.lineEdit_5.setClearButtonEnabled(True)
        self.lineEdit_4.setClearButtonEnabled(True)
        self.textEdit_2.setReadOnly(True)
        self.lineEdit_7.setClearButtonEnabled(True)
        self.lineEdit_8.setClearButtonEnabled(True)
        # 设置单选默认选择项
        # self.radioButton_6.setChecked(True)
        # 设置窗口名称
        self.setWindowTitle("测试用例生成工具V2.0")
        # 设置输入框提示
        self.lineEdit_2.setPlaceholderText("填接口地址即可，不需要ip和port")
        self.lineEdit_4.setPlaceholderText("测试用例文件的存储目录")
        # 工具栏
        self.actionMD5jia.setText("MD5加密")
        self.actionbase64.setText("base64加密")
        self.actionsha1.setText("sha1加密")

    def load_directory(self):
        BASE_DIR = os.path.dirname(os.path.dirname(__file__))
        base_testCase = os.path.join(BASE_DIR, 'testcase')
        if not os.path.exists(base_testCase):
            os.mkdir(base_testCase)
        else:
            pass
        return base_testCase

    def test_case_filename(self):
        case_filename = self.lineEdit_6.text().strip()

        if case_filename == "":
            self.bounced("测试用例文件名不能为空！")
        return case_filename

    def open_file(self):
        # file_name返回的是一个元组，第一个参数为文件名，第二个为文件类型
        file_name = QFileDialog.getOpenFileName(self, "选取文件", "./", "All Files (*);;Excel Files (*.xls)")
        # return file_name
        self.lineEdit_10.setText(file_name[0])

    def open_generate_file(self):
        file_name = QFileDialog.getExistingDirectory(self, "选择测试用例存储路径", self.load_directory())
        self.lineEdit_5.setText(file_name)

    def create_testcase_directory(self):
        root_dir = self.load_directory()
        creat_dir = self.lineEdit_4.text()

        test_case_filepth = root_dir + "\\" + creat_dir
        # 判断路径是否存在
        isExists = os.path.exists(test_case_filepth)
        if not isExists:
            os.mkdir(test_case_filepth)
            self.logging_out(self.info_log_text('目录【%s】创建成功！' % creat_dir))
        else:
            self.logging_out(self.error_log_text('目录："%s" 已存在' % test_case_filepth))

        return test_case_filepth

    def get_current_time(self):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return current_time

    def info_log_text(self, msg):
        current_time = self.get_current_time()
        self.textEdit_2.setStyleSheet('background-color: white;'
                                      'color: green;'
                                      'font: normal 11pt "Times New Roman";')
        logs_msg = str(current_time) + "-" + "[INFO]" + "-" + str(msg)
        return logs_msg

    def error_log_text(self, msg):
        current_time = self.get_current_time()
        self.textEdit_2.setStyleSheet('background-color: white;'
                                      'color: red;'
                                      'font: normal 11pt "Times New Roman";')
        logs_msg = str(current_time) + "-" + "[ERROR]" + "-" + str(msg)
        return logs_msg

    def write_yaml_data(self, filepath, data):
        # allow_unicode=True：处理中文
        test_file_name = self.test_case_filename()
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                if test_file_name != '':
                    yaml.dump(data, f, allow_unicode=True, sort_keys=False)
                    self.logging_out(self.info_log_text("测试用例文件生成成功!"))
        except Exception:
            self.logging_out(self.error_log_text(str(traceback.format_exc())))

    def testcase_baseinfo_template(self):
        header = self.get_header()
        if header != "":
            base_info = {
                'api_name': self.get_api_name(),
                'url': self.get_url(),
                'method': self.get_method(),
                'header': header
            }
        else:
            base_info = {
                'api_name': self.get_api_name(),
                'url': self.get_url(),
                'method': self.get_method(),
            }
        return base_info

    def testcase_template(self):
        self.radioButtonGroup_3 = QtWidgets.QButtonGroup(self.groupBox_2)
        # 将第一组单选按钮加入到分组中,并设置按钮id

        self.radioButtonGroup_3.addButton(self.radioButton_3, 1003)
        self.radioButtonGroup_3.addButton(self.radioButton_4, 1004)
        # 获取依赖类型属性id
        depend_id = self.radioButtonGroup_3.checkedId()
        depend_params = self.get_depend_params()

        try:
            testcase = {
                1003: [{
                    'case_name': self.case_name(),
                    self.request_params()[0]: self.request_params()[1],
                    'validation': self.get_assert_params(),
                    ''.join(list(depend_params.keys())): list(depend_params.values())[0]
                }],
                1004: [{
                    'case_name': self.case_name(),
                    self.request_params()[0]: self.request_params()[1],
                    'validation': self.get_assert_params()
                }]
            }

            testcase_data = testcase[depend_id]
            # 判断files标签页中table表格中是否有数据，有的话追加到字典中
            file_tab = self.get_files()
            if file_tab:
                for value in testcase.values():
                    value[0]['data'] = file_tab

            return testcase_data

        except Exception:
            self.logging_out(self.error_log_text(str(traceback.format_exc())))

    def all_template(self):
        base_info = self.testcase_baseinfo_template()
        test_case = self.testcase_template()
        base_info_all = [
            {
                'baseInfo': base_info,
                'testCase': test_case
            }
        ]
        return base_info_all

    def generate_testcase_file(self):
        test_file_path = self.lineEdit_5.text().strip()
        test_file_name = self.test_case_filename()
        test_data = self.all_template()
        path_join = test_file_path + '\\' + test_file_name + '.yaml'
        self.write_yaml_data(path_join, test_data)

    def logging_out(self, text):
        # 获取文本光标对象
        cursor = self.textEdit_2.textCursor()
        # 设置字体颜色
        # self.textEdit_2.setStyleSheet('background-color: white;'
        #                               'color: %s;'
        #                               'font: bold italic 11pt "Times New Roman";color：green;')
        # 移动光标
        cursor.movePosition(QtGui.QTextCursor.End)
        # 输出日志换行
        self.textEdit_2.append(cursor.insertText(text))
        # 把文本光标设置回去
        self.textEdit_2.setTextCursor(cursor)
        self.textEdit_2.ensureCursorVisible()

    def update_text(self, message):
        """更新日志信息"""
        self.textEdit_2.append(message)

    def get_host(self):
        ip = self.lineEdit_7.text()
        return ip

    def get_port(self):
        port = self.lineEdit_8.text()
        return port

    def api_debug_button(self):
        method = self.get_method()
        ip = self.get_host()
        port = self.get_port()
        url_text = self.get_url()
        protocol = self.comboBox_2.currentText()
        if port != "":
            url = protocol + '://' + ip + ':' + port + url_text
        else:
            url = protocol + '://' + ip + url_text
        header = self.get_header()
        if header:
            header = header
        handle_params = self.request_params()[1]
        param_type = self.request_params()[0]
        request_param = {param_type: handle_params}
        files = self.get_files()
        try:
            requests.packages.urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            res = requests.request(url=url, method=method, headers=header, files=files, verify=False, **request_param)
            self.bounced(res.text, title='接口请求结果')
        except Exception:
            self.logging_out(self.error_log_text(str(traceback.format_exc())))

    def clear_log(self):
        """清空日志"""
        self.textEdit_2.clear()

    def other_func(self):
        self.pushButton_14.clicked.connect(self.create_testcase_directory)
        self.pushButton_15.clicked.connect(self.open_generate_file)
        self.pushButton_17.clicked.connect(self.generate_testcase_file)
        self.pushButton_16.clicked.connect(self.api_debug_button)
        self.pushButton_19.clicked.connect(self.clear_log)
        # 点击工具菜单栏触发弹窗事件
        self.actionMD5jia.triggered.connect(self.open_md5_window)
        self.actionbase64.triggered.connect(self.open_base64_window)
        self.actionsha1.triggered.connect(self.open_sha1_window)

    def open_md5_window(self):
        """打开md5加密子窗口"""
        # 显示子窗口
        self.child_win.show()
        # 连接信号
        self.child_win._signal.connect(self.get_md5_data)

    def open_base64_window(self):
        """打开base64加密子窗口"""
        # 显示子窗口
        self.child_win_base64.show()
        # 连接信号
        self.child_win_base64._signal.connect(self.get_base64_data)

    def open_sha1_window(self):
        """打开base64加密子窗口"""
        # 显示子窗口
        self.child_win_sha1.show()
        # 连接信号
        self.child_win_sha1._signal.connect(self.get_sha1_data)

    def get_md5_data(self):
        """主窗口获取子窗口的值"""
        pass

    def get_base64_data(self):
        """主窗口获取子窗口的值"""
        pass

    def get_sha1_data(self):
        """主窗口获取子窗口的值"""
        pass


# 界面样式设置
stylesheet = """
/* QPushButton#xxx或者#xx都表示通过设置的objectName来指定 */
QPushButton#pushButton_17{
     background-color: #76a5af; /*背景颜色*/
     font: bold normal 11pt;
     border-radius: 10px; /*圆角*/
}
#pushButton_17:hover {
    background-color: #648f98; /*鼠标悬停时背景颜色*/
}
QPushButton#pushButton_16{
     background-color: #76a5af; /*背景颜色*/
     font: bold normal 11pt;
     border-radius: 10px; /*圆角*/
}
#pushButton_16:hover {
    background-color: #648f98; /*鼠标悬停时背景颜色*/
}
QLineEdit{
     border-radius: 5px; /*圆角*/
     border:0.5px solid;
}
QComboBox{
     border-radius: 5px; /*圆角*/
     border:0.5px solid;
}
QPushButton#pushButton_18{
     background-color: #76a5af; /*背景颜色*/
     font: bold normal 11pt;
     border-radius: 10px; /*圆角*/
}
#pushButton_18:hover {
    background-color: #648f98; /*鼠标悬停时背景颜色*/
}
QPushButton#pushButton_14{
     background-color: #76a5af; /*背景颜色*/
     font: bold normal 11pt;
     border-radius: 5px; /*圆角*/
}
#pushButton_14:hover {
    background-color: #648f98; /*鼠标悬停时背景颜色*/
}
QPushButton#pushButton_15{
     background-color: #76a5af; /*背景颜色*/
     border-radius: 5px; /*圆角*/
}
#pushButton_15:hover {
    background-color: #648f98; /*鼠标悬停时背景颜色*/
}
#pushButton_3{
     background-color: #cfdff9; /*背景颜色*/
     border-radius: 5px; /*圆角*/
}
#pushButton_3:hover {
    background-color: #acc7f4; /*鼠标悬停时背景颜色*/
}
/*界面背景色设置*/
QWidget#MainWindow{
    background-color:#f6f8fd;
}
"""


# 子窗口-MD5
class ToolMD5Window(QtWidgets.QMainWindow):
    # 自定义信号（str类型），必须在init初始化前定义
    _signal = pyqtSignal(str, str)

    def __init__(self):
        super(ToolMD5Window, self).__init__()
        self.setupUI(self)

    def setupUI(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(583, 385)
        # 设置窗体属性，子窗口弹出后，父窗口不可操作
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(20, 10, 551, 331))
        self.groupBox_3.setObjectName("groupBox_3")
        self.groupBox = QtWidgets.QGroupBox(self.groupBox_3)
        self.groupBox.setGeometry(QtCore.QRect(0, 20, 541, 131))
        self.groupBox.setObjectName("groupBox")
        self.textEdit = QtWidgets.QTextEdit(self.groupBox)
        self.textEdit.setGeometry(QtCore.QRect(10, 20, 521, 101))
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setText("")
        self.groupBox_2 = QtWidgets.QGroupBox(self.groupBox_3)
        self.groupBox_2.setGeometry(QtCore.QRect(0, 160, 541, 121))
        self.groupBox_2.setObjectName("groupBox_2")
        self.textEdit_2 = QtWidgets.QTextEdit(self.groupBox_2)
        self.textEdit_2.setGeometry(QtCore.QRect(10, 20, 521, 91))
        self.textEdit_2.setObjectName("textEdit_2")
        self.textEdit_2.setText("")
        self.pushButton = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton.setGeometry(QtCore.QRect(150, 290, 91, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_2.setGeometry(QtCore.QRect(280, 290, 91, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 583, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # 设置窗口信息
        MainWindow.setWindowTitle("MD5加密")
        self.groupBox_3.setTitle("MD5加密")
        self.groupBox.setTitle("待输出数据")
        self.groupBox_2.setTitle("结果")
        self.pushButton.setText("加密")
        self.pushButton_2.setText("清空")
        self.textEdit_2.setReadOnly(True)
        self.textEdit.setAcceptRichText(False)

        # 点击按钮
        self.pushButton.clicked.connect(self.set_md5_value)
        self.pushButton_2.clicked.connect(self._clear)

    def sha1_encryption(self):
        """参数sha1加密"""
        enc_data = sha1()
        # 获取待输出数据
        params = self.textEdit.toPlainText()
        enc_data.update(params.encode(encoding="utf-8"))
        return enc_data.hexdigest()

    def set_md5_value(self):
        md5_data = self.sha1_encryption()
        self.textEdit_2.setText(md5_data)

    def _clear(self):
        self.textEdit.clear()
        self.textEdit_2.clear()


# 子窗口-base64
class ToolBase64Window(QtWidgets.QMainWindow):
    # 自定义信号（str类型），必须在init初始化前定义
    _signal = pyqtSignal(str, str)

    def __init__(self):
        super(ToolBase64Window, self).__init__()
        self.setupUI(self)

    def setupUI(self, MainWindow):
        MainWindow.setObjectName("MainWindow_2")
        MainWindow.resize(583, 385)
        # 设置窗体属性，子窗口弹出后，父窗口不可操作
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(20, 10, 551, 331))
        self.groupBox_3.setObjectName("groupBox_3")
        self.groupBox = QtWidgets.QGroupBox(self.groupBox_3)
        self.groupBox.setGeometry(QtCore.QRect(0, 20, 541, 131))
        self.groupBox.setObjectName("groupBox")
        self.textEdit = QtWidgets.QTextEdit(self.groupBox)
        self.textEdit.setGeometry(QtCore.QRect(10, 20, 521, 101))
        self.textEdit.setObjectName("textEdit")
        self.groupBox_2 = QtWidgets.QGroupBox(self.groupBox_3)
        self.groupBox_2.setGeometry(QtCore.QRect(0, 160, 541, 121))
        self.groupBox_2.setObjectName("groupBox_2")
        self.textEdit_2 = QtWidgets.QTextEdit(self.groupBox_2)
        self.textEdit_2.setGeometry(QtCore.QRect(10, 20, 521, 91))
        self.textEdit_2.setObjectName("textEdit_2")
        self.pushButton = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton.setGeometry(QtCore.QRect(150, 290, 91, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_2.setGeometry(QtCore.QRect(280, 290, 91, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 583, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # 设置窗口信息
        MainWindow.setWindowTitle("Base64加密")
        self.groupBox_3.setTitle("Base64加密")
        self.groupBox.setTitle("待输出数据")
        self.groupBox_2.setTitle("结果")
        self.pushButton.setText("加密")
        self.pushButton_2.setText("清空")
        self.textEdit_2.setReadOnly(True)
        self.textEdit.setAcceptRichText(False)

        # 点击按钮
        self.pushButton.clicked.connect(self.set_base64_value)
        self.pushButton_2.clicked.connect(self._clear)

    def base64_encryption(self):
        """base64加密"""
        params = self.textEdit.toPlainText()
        base_params = params.encode("utf-8")
        encr = base64.b64encode(base_params)
        return encr

    def set_base64_value(self):
        base64_data = self.base64_encryption()
        self.textEdit_2.setText(str(base64_data))

    def _clear(self):
        self.textEdit.clear()
        self.textEdit_2.clear()


# 子窗口-sha1加密
class ToolSha1Window(QtWidgets.QMainWindow):
    # 自定义信号（str类型），必须在init初始化前定义
    _signal = pyqtSignal(str, str)

    def __init__(self):
        super(ToolSha1Window, self).__init__()
        self.setupUI(self)

    def setupUI(self, MainWindow):
        MainWindow.setObjectName("MainWindow_3")
        MainWindow.resize(583, 385)
        # 设置窗体属性，子窗口弹出后，父窗口不可操作
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(20, 10, 551, 331))
        self.groupBox_3.setObjectName("groupBox_3")
        self.groupBox = QtWidgets.QGroupBox(self.groupBox_3)
        self.groupBox.setGeometry(QtCore.QRect(0, 20, 541, 131))
        self.groupBox.setObjectName("groupBox")
        self.textEdit = QtWidgets.QTextEdit(self.groupBox)
        self.textEdit.setGeometry(QtCore.QRect(10, 20, 521, 101))
        self.textEdit.setObjectName("textEdit")
        self.groupBox_2 = QtWidgets.QGroupBox(self.groupBox_3)
        self.groupBox_2.setGeometry(QtCore.QRect(0, 160, 541, 121))
        self.groupBox_2.setObjectName("groupBox_2")
        self.textEdit_2 = QtWidgets.QTextEdit(self.groupBox_2)
        self.textEdit_2.setGeometry(QtCore.QRect(10, 20, 521, 91))
        self.textEdit_2.setObjectName("textEdit_2")
        self.pushButton = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton.setGeometry(QtCore.QRect(150, 290, 91, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_2.setGeometry(QtCore.QRect(280, 290, 91, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 583, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # 设置窗口信息
        MainWindow.setWindowTitle("Sha1加密")
        self.groupBox_3.setTitle("Sha1加密")
        self.groupBox.setTitle("待输出数据")
        self.groupBox_2.setTitle("结果")
        self.pushButton.setText("加密")
        self.pushButton_2.setText("清空")
        # 设置不可输入
        self.textEdit_2.setReadOnly(True)
        self.textEdit.setAcceptRichText(False)

        # 点击按钮
        self.pushButton.clicked.connect(self.set_sha1_value)
        self.pushButton_2.clicked.connect(self._clear)

    def sha1_encryption(self):
        """参数sha1加密"""
        enc_data = sha1()
        params = self.textEdit.toPlainText()
        enc_data.update(params.encode(encoding="utf-8"))
        return enc_data.hexdigest()

    def set_sha1_value(self):
        sha_data = self.sha1_encryption()
        self.textEdit_2.setText(str(sha_data))

    def _clear(self):
        self.textEdit.clear()
        self.textEdit_2.clear()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(stylesheet)
    ui = NewTestCaseTools()
    ui.show()
    sys.exit(app.exec_())
