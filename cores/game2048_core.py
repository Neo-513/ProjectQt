from uis.game2048 import Ui_MainWindow
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import numpy as np
import random
import sys


class Core(QMainWindow, Ui_MainWindow):
	ROTATES = {
		Qt.Key_Up: 1,
		Qt.Key_Down: -1,
		Qt.Key_Left: 0,
		Qt.Key_Right: 2,
	}  # 矩阵旋转角度

	STYLE_BORDER = "border-width: 1px;border-style: solid;border-color: black;"  # 矩阵边框样式
	STYLE_COLOR = {
		0: "245,222,179", 2: "255,227,132", 4: "227,207,87", 8: "227,168,105", 16: "255,215,0", 32: "255,255,0",
		64: "255,153,18", 128: "237,145,33", 256: "255,97,0", 512: "255,0,0", 1024: "227,23,13", 2048: "178,34,34"
	}  # 矩阵颜色

	def __init__(self):
		super(Core, self).__init__(None)  # 初始化
		self.setupUi(self)  # 启动
		self.setFixedSize(self.width(), self.height())  # 设置页面大小固定
		self.setWindowTitle("2048")  # 设置标题

		'''绑定按钮事件'''
		self.pushButton_start.clicked.connect(self.start)

		'''标签组'''
		self.labels = (
			(self.label_00, self.label_01, self.label_02, self.label_03),
			(self.label_10, self.label_11, self.label_12, self.label_13),
			(self.label_20, self.label_21, self.label_22, self.label_23),
			(self.label_30, self.label_31, self.label_32, self.label_33),
		)  # 标签组（用于展示矩阵）
		for labels in self.labels:
			for label in labels:
				label.setStyleSheet(self.STYLE_BORDER)  # 设置样式
				label.setAlignment(Qt.AlignCenter)  # 设置居中
				label.setFont(QFont("Microsoft YaHei", 15, QFont.Bold))  # 设置字体

		'''全局变量'''
		self.matrix, self.score, self.step, self.game_state = None, 0, 0, 0  # 矩阵、得分、步数、游戏状态

		'''设定特定控件失焦'''
		for child in self.children():  # 遍历控件组
			if isinstance(child, QWidget):  # 控件
				for c in child.children():  # 遍历控件
					if isinstance(c, QPushButton):  # 按钮
						c.setFocusPolicy(Qt.NoFocus)  # 设置失焦（实现监听上下左右按件）

		'''其他'''
		self.start()

	def start(self):  # 开始游戏
		self.matrix = np.zeros((4, 4), dtype=int)  # 初始化矩阵
		self.score = 0  # 初始化分数
		self.step = 0  # 初始化步数
		self.game_state = 0  # 初始化游戏状态

		self.add_num(2)  # 初始数字
		self.add_num(2)  # 初始数字
		self.display()

	def keyPressEvent(self, event):  # 键盘监听事件
		self.run(event.key())

	def run(self, key_press):
		if key_press not in self.ROTATES:  # 非目标键位
			return

		prev_state = self.matrix.copy()  # 矩阵前一状态
		self.matrix = np.rot90(self.matrix, self.ROTATES[key_press])  # 旋转矩阵
		self.merge()
		self.matrix = np.rot90(self.matrix, -self.ROTATES[key_press])  # 逆旋转矩阵

		if self.matrix.tolist() != prev_state.tolist():  # 矩阵状态发生改变
			self.add_num()
			self.step += 1
			self.display()

		self.game_state = self.update_state()
		if self.game_state == 1:  # 游戏胜利
			self.show_message(f"游戏胜利！得分{self.score}，步数{self.step}")
			self.start()
		elif self.game_state == -1:  # 游戏结束
			self.show_message(f"游戏结束！得分{self.score}，步数{self.step}")
			self.start()

	def merge(self):  # 合并数字算法（通过旋转矩阵将所有的合并操作转化为从右向左合并）
		for i, row_old in enumerate(self.matrix):
			row_new = []  # 新建行
			raw = True  # 未合并过的数字
			for cell in row_old:
				if cell != 0:
					if row_new and row_new[-1] == cell and raw:  # 合并数字
						row_new[-1] += cell
						raw = False
						self.score += row_new[-1]
					else:
						row_new.append(cell)  # 移动数字
						raw = True

			row_new.extend(0 for _ in range(4 - len(row_new)))  # 补0
			self.matrix[i] = row_new  # 新建行代替原有行

	def add_num(self, num=None):  # 新增数字
		blanks = [(i * 4 + j) for i, row in enumerate(self.matrix) for j, cell in enumerate(row) if cell == 0]  # 空位
		blank = random.choice(blanks)  # 随机选择位置
		num = num if num else random.choice([2, 4])  # 随机生成2或4
		self.matrix[int(blank / 4)][blank % 4] = num  # 矩阵赋值

	def update_state(self):  # 更新游戏状态
		if sum([cell == 2048 for row in self.matrix for cell in row]) == 1:  # 合成了2048
			return 1  # 游戏胜利

		m = self.matrix.copy()  # 按行计算
		m_t = np.rot90(m, 1)  # 按列计算
		for i in range(3):
			if 0 in (m[i + 1] - m[i]) or 0 in (m_t[i + 1] - m_t[i]):  # 有相邻且相同的数字
				return 0  # 游戏继续
		if [(i * 4 + j) for i, row in enumerate(self.matrix) for j, cell in enumerate(row) if cell == 0]:  # 有空位
			return 0  # 游戏继续

		return -1  # 游戏结束

	def display(self):  # 展示矩阵
		for i, row in enumerate(self.matrix):
			for j, cell in enumerate(row):
				self.labels[i][j].setText(str(cell) if cell else "")
				self.labels[i][j].setStyleSheet(f"background-color: rgb({self.STYLE_COLOR[cell]});{self.STYLE_BORDER}")
		self.label_score.setText(f"SCORE: {self.score}")
		self.label_step.setText(f"STEP: {self.step}")

	@staticmethod
	def show_message(text=""):  # 弹窗提示
		message_box = QMessageBox()
		message_box.setWindowTitle("提示")
		message_box.setText(text)
		message_box.exec_()


if __name__ == "__main__":
	QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)  # 自动适应高分辨率
	app = QApplication(sys.argv)  # 创建app（sys.argv是命令行参数列表）
	myWindow = Core()  # 初始化
	myWindow.show()  # 显示窗口控件
	sys.exit(app.exec_())  # 完整退出
