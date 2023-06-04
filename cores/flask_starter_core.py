from uis.flask_starter import Ui_MainWindow
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import pyperclip
import os
import sys
import time


class Core(QMainWindow, Ui_MainWindow):
	ports = {
		"ProjectDatabase": 8081,
		"ProjectSearchEngine": 8082,
		"ProjectWorkPasswords": 8083
	}

	def __init__(self):
		super(Core, self).__init__(None)  # 初始化
		self.setupUi(self)  # 启动
		self.setFixedSize(self.width(), self.height())  # 设置页面大小固定
		self.setWindowTitle("flask启动器")  # 设置标题

		'''绑定按钮事件'''
		self.pushButton_start.clicked.connect(self.start)
		self.pushButton_copy.clicked.connect(self.copy)

		'''下拉框赋值'''
		self.comboBox_url.addItem("", 0)
		for port in self.ports:
			self.comboBox_url.addItem(port, self.comboBox_url.size())

		'''其他'''
		self.textEdit_log.setReadOnly(True)  # 设置只读
		self.textEdit_log.setLineWrapMode(False)  # 取消自动换行

	def start(self):  # 启动
		project, url = self.copy()
		if project and url:
			command = f"@echo off & d: & cd d:/python & start python d:/workspace_PyCharm/{project}/server.py"  # 启动命令
			os.system(command)  # 执行启动命令
			self.log(url)

	def copy(self):  # 复制地址
		project = self.comboBox_url.itemText(self.comboBox_url.currentIndex())
		if project:
			url = f"http://127.0.0.1:{self.ports[project]}/"
			pyperclip.copy(url)  # 添加至剪切板
			return project, url
		return None, None

	def log(self, msg):  # 打印日志
		current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # 当前时间
		self.textEdit_log.moveCursor(QTextCursor.End)  # 光标移动到最后
		if self.textEdit_log.toPlainText().strip():
			self.textEdit_log.insertPlainText("\n\n")
		self.textEdit_log.insertPlainText(f"[{current_time}]    {msg}")  # 打印日志
		self.textEdit_log.moveCursor(self.textEdit_log.textCursor().End)  # 滚动条到最底


if __name__ == "__main__":
	QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)  # 自动适应高分辨率
	app = QApplication(sys.argv)  # 创建app（sys.argv是命令行参数列表）
	myWindow = Core()  # 初始化
	myWindow.show()  # 显示窗口控件
	sys.exit(app.exec_())  # 完整退出
