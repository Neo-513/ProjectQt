from uis.exe_packer import Ui_MainWindow
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import os
import sys
import time


class Core(QMainWindow, Ui_MainWindow):
	FOLDERPATH = "D:/workspace_PyCharm/ProjectQt/cores"  # 默认文件路径

	def __init__(self):
		super(Core, self).__init__(None)  # 初始化
		self.setupUi(self)  # 启动
		self.setFixedSize(self.width(), self.height())  # 设置页面大小固定
		self.setWindowTitle("exe打包工具")  # 设置标题

		'''绑定按钮事件'''
		self.pushButton_impt.clicked.connect(self.impt)
		self.pushButton_pack.clicked.connect(self.pack)

		'''其他'''
		self.filename = None  # 文件名
		self.textEdit_log.setReadOnly(True)  # 设置只读
		self.textEdit_log.setLineWrapMode(False)  # 取消自动换行

	def impt(self):  # 导入
		filepath = QFileDialog.getOpenFileName(
			self, filter="*.py", directory=self.FOLDERPATH, options=QFileDialog.Options()
		)[0].strip()  # 文件对话框
		if filepath:
			self.filename = filepath.split("/")[-1][:-3]
			self.log(f"导入: {filepath}")

	def pack(self):  # 打包
		if self.filename:
			command = f"d: & cd {self.FOLDERPATH} & pyinstaller -F -w {self.filename}.py"  # 打包命令
			os.system(command)  # 执行打包命令
			self.log(f"打包命令: {command}")
			self.log(f"打包完成: {self.FOLDERPATH}/dist/{self.filename}.exe")
			self.filename = None  # 重置文件路径

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
