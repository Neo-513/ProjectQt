from uis.handwriting_recognition import Ui_MainWindow
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import cv2
import numpy as np
import os
import torch
import sys


class Core(QMainWindow, Ui_MainWindow):
	DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")  # 运算设备
	PATH_MODEL = "D:/workspace_PyCharm/projectDeepLearning/models/model_handwriting_recognition.pt"  # 运算模型绝对路径
	PIXEL2RGB = {
		4278190080: (qBlue(4278190080), qGreen(4278190080), qRed(4278190080)),  # 黑
		4294967295: (qBlue(4294967295), qGreen(4294967295), qRed(4294967295))  # 白
	}  # 像素对应的rgb值

	def __init__(self):
		super(Core, self).__init__(None)  # 初始化
		self.setupUi(self)  # 启动
		self.setFixedSize(self.width(), self.height())  # 设置页面大小固定
		self.setWindowTitle("识别手写数字")  # 设置标题

		'''绑定按钮事件'''
		self.pushButton_recognize.clicked.connect(self.recognize)
		self.pushButton_clear.clicked.connect(self.clear)

		'''全局变量'''
		self.model = NerualNetwork(28 * 28, 500, 10).to(self.DEVICE)  # 运算模型
		self.default_pixmap = self.cvimg2qpix(np.zeros((28, 28), dtype=np.uint8))  # 默认像素映射

		'''其他'''
		self.clear()

	def recognize(self):
		if not self.paintboard.is_empty():
			with torch.no_grad():  # 局域内不计算梯度
				if os.path.exists(self.PATH_MODEL):
					self.model.load_state_dict(torch.load(self.PATH_MODEL, map_location=self.DEVICE))  # 加载模型参数

				img_resized = self.get_resized()  # 缩放后的画板图像
				self.label_img.setPixmap(self.cvimg2qpix(img_resized))  # 展示像素映射
				img_array = np.array(img_resized, np.float32)  # 转为数组
				img_tensor = torch.from_numpy(img_array)  # 转为张量
				img_dimension = img_tensor.reshape(-1, 28 * 28).to(self.DEVICE)  # 数组降维

				outputs = self.model(img_dimension)  # 正向传播计算预测值
				output = np.argmax(outputs.cpu().detach().numpy(), axis=1)[0]  # 获取输出
				self.label_result.setText(f"识别结果: {output}")  # 展示识别结果

	def clear(self):  # 清空
		self.paintboard.clear()  # 重置画板
		self.label_img.setPixmap(self.default_pixmap)  # 重置像素映射
		self.label_result.setText("识别结果:")

	def get_resized(self):  # 获取缩放后的画板图像
		qimg = self.paintboard.get_img()  # 获取画板图像
		cvimg = self.qimg2cvimg(qimg)  # 转为图像矩阵
		img_gray = cv2.cvtColor(cvimg, cv2.COLOR_RGB2GRAY)  # 灰度处理
		_, img_threshold = cv2.threshold(
			img_gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)  # 大津算法进行二值化处理并反转
		img_resized = cv2.resize(img_threshold, (28, 28))  # 将图片大小缩放到与训练集图片一致
		return img_resized

	def qimg2cvimg(self, qimg):  # 将画板图像转为图像矩阵
		cvimg = np.zeros((qimg.height(), qimg.width(), 3), dtype=np.uint8)
		for row in range(qimg.height()):
			for col in range(qimg.width()):
				cvimg[row, col] = self.PIXEL2RGB[qimg.pixel(col, row)]
		return cvimg

	@staticmethod
	def cvimg2qpix(cvimg):  # 将图像矩阵转为像素映射
		height, width = cvimg.shape
		qimg = QImage(cvimg.data, width, height, width, QImage.Format_Indexed8)
		qpix = QPixmap().fromImage(qimg, flags=Qt.AutoColor)
		return qpix


class NerualNetwork(torch.nn.Module):
	def __init__(self, input_size, hidden_size, output_size):
		super(NerualNetwork, self).__init__()
		self.l1 = torch.nn.Linear(input_size, hidden_size)  # 第一层线性模型（传入输入层和隐藏层）
		self.relu = torch.nn.ReLU()  # relu激活函数
		self.l2 = torch.nn.Linear(hidden_size, output_size)  # 第二层线性模型（传入隐藏层和输出层）

	def forward(self, x):  # 重写正向传播函数（获取预测值）
		output = self.l1(x)  # 第一层线性模型
		output = self.relu(output)  # relu激活函数
		output = self.l2(output)  # 第二层线性模型
		return output


if __name__ == "__main__":
	QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)  # 自动适应高分辨率
	app = QApplication(sys.argv)  # 创建app（sys.argv是命令行参数列表）
	myWindow = Core()  # 初始化
	myWindow.show()  # 显示窗口控件
	sys.exit(app.exec_())  # 完整退出
