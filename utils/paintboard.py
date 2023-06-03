from PyQt5.QtWidgets import QWidget
from PyQt5.Qt import QPixmap, QPainter, QPoint, QPen, QSize
from PyQt5.QtCore import Qt


class PaintBoard(QWidget):
	def __init__(self, parent=None):
		super().__init__(parent=parent)  # 初始化

		'''全局变量'''
		self.__board = QPixmap(QSize(400, 400))  # 画板
		self.__painter = QPainter()  # 绘图工具
		self.__pos_prev = QPoint(0, 0)  # 鼠标前一位置
		self.__is_empty = True  # 是否为空

	def get_img(self):  # 获取画板内容
		return self.__board.toImage()

	def is_empty(self):
		return self.__is_empty

	def clear(self):  # 清空画板
		self.__board.fill(Qt.white)  # 用白色填充画板
		self.__is_empty = True
		self.update()  # 更新显示

	def paintEvent(self, paintEvent):  # 绘图事件
		self.__painter.begin(self)  # 启动画板
		self.__painter.drawPixmap(0, 0, self.__board)  # 绘制画板
		self.__painter.end()  # 结束画板

	def mousePressEvent(self, mouseEvent):  # 鼠标按下事件
		self.__pos_prev = mouseEvent.pos()  # 更新鼠标前一位置
		self.__is_empty = False

	def mouseMoveEvent(self, mouseEvent):  # 鼠标移动事件
		pos_curr = mouseEvent.pos()  # 获取鼠标当前位置
		self.__painter.begin(self.__board)  # 启动画笔
		self.__painter.setPen(QPen(Qt.black, 15))  # 设置画笔颜色、粗细
		self.__painter.drawLine(self.__pos_prev, pos_curr)  # 绘制线条
		self.__painter.end()  # 结束画笔
		self.__pos_prev = pos_curr  # 更新鼠标前一位置
		self.__is_empty = False
		self.update()  # 更新显示
