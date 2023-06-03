from PyQt5.QtWidgets import QCheckBox, QComboBox, QLineEdit, QListWidget, QListWidgetItem


class MyComBox(QComboBox):
	def __init__(self, parent=None):
		super(MyComBox, self).__init__(parent=parent)  # 初始化
		self.items, self.check_boxes = None, None  # 元素集合、勾选框集合

		self.qLineEdit = QLineEdit()  # 文本框对象
		self.qLineEdit.setReadOnly(True)  # 设置只读
		self.setLineEdit(self.qLineEdit)  # 绑定文本框对象

	def set_items(self, items):  # 设置元素
		self.items = items.copy()  # 元素集合
		self.items.insert(0, "全部")

		list_widget = QListWidget()  # 下拉列表
		self.check_boxes = [QCheckBox() for _ in range(len(self.items))]  # 勾选框集合
		for i, item in enumerate(self.items):
			self.check_boxes[i].setText(item)  # 设置内容
			self.check_boxes[i].stateChanged.connect(self._select_all if i == 0 else self._select)  # 绑定事件
			list_widget.setItemWidget(QListWidgetItem(list_widget), self.check_boxes[i])  # 勾选框绑定到下拉列表

		self.setModel(list_widget.model())  # 绑定模型
		self.setView(list_widget)  # 绑定视图
		self.setMaxVisibleItems(100)  # 避免滚动条覆盖标签

	def get_items(self):  # 获取勾选的元素
		return [self.check_boxes[i].text() for i in range(1, len(self.items)) if self.check_boxes[i].isChecked()]

	def _select(self):  # 单个元素勾选事件
		checked_items = self.get_items()  # 获取勾选的元素
		self.qLineEdit.setText(";".join(checked_items))  # 设置文本

		if not checked_items:
			self.check_boxes[0].setCheckState(0)  # 未勾选
		elif len(checked_items) == len(self.items) - 1:
			self.check_boxes[0].setCheckState(2)  # 全选
		else:
			self.check_boxes[0].setCheckState(1)  # 部分勾选

	def _select_all(self, state):  # 全选事件
		if state == 2:  # 全选
			for i in range(1, len(self.items)):
				self.check_boxes[i].setChecked(True)
		elif state == 1:  # 部分勾选
			for i in range(1, len(self.items)):
				if self.check_boxes[i].isChecked():
					return
			self.check_boxes[0].setCheckState(2)
		elif state == 0:  # 未勾选
			for i in range(len(self.items)):
				self.check_boxes[i].setChecked(False)
