from uis.code_supporter import Ui_MainWindow
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import pyperclip
import sys


class Core(QMainWindow, Ui_MainWindow):
	HEADERS = [" ", "参数名", "赋值方式"]
	ASSIGNMENT = ["字符串拼接", "@拼接"]
	CONNECTOR = ["= param", "LIKE '%' || param || '%'"]

	def __init__(self):
		super(Core, self).__init__(None)  # 初始化
		self.setupUi(self)  # 启动
		self.setFixedSize(self.width(), self.height())  # 设置页面大小固定
		self.setWindowTitle("代码辅助工具")  # 设置标题

		'''绑定按钮事件'''
		self.pushButton_quote.clicked.connect(self.quote)
		self.pushButton_unquote.clicked.connect(self.unquote)
		self.pushButton_upper.clicked.connect(self.upper)
		self.pushButton_lower.clicked.connect(self.lower)
		self.pushButton_copy1.clicked.connect(self.copy1)
		self.pushButton_clear1.clicked.connect(self.clear1)

		self.pushButton_add.clicked.connect(self.add)
		self.pushButton_delete.clicked.connect(self.delete)
		self.pushButton_generatesql.clicked.connect(self.generate_sql)
		self.pushButton_copy2.clicked.connect(self.copy2)
		self.pushButton_clear2.clicked.connect(self.clear2)

		'''设置只读'''
		self.textEdit_output1.setReadOnly(True)
		self.textEdit_output2.setReadOnly(True)

		'''取消自动换行'''
		self.textEdit_output1.setLineWrapMode(False)
		self.textEdit_output2.setLineWrapMode(False)

		'''新增列及设置表头'''
		self.tableWidget_input2.setColumnCount(len(self.HEADERS))  # 设置列数
		for i, header in enumerate(self.HEADERS):
			self.tableWidget_input2.setHorizontalHeaderItem(i, QTableWidgetItem(header))

		'''其他'''
		self.comboBox_assignment.addItems(self.ASSIGNMENT)  # 下拉框赋值
		self.tableWidget_input2.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)  # 自适应列宽

	"""基础功能"""
	def quote(self):  # 加引号
		text = self.textEdit_input1.toPlainText()
		if text.strip():
			lines = [f"\"{'' if line.startswith(' ') else ' '}{line.rstrip()}\"" for line in text.split("\n")]
			self.textEdit_output1.setText("\n".join(lines) + ";")

	def unquote(self):  # 去引号
		text = self.textEdit_input1.toPlainText()
		if text.strip():
			lines = [line.rstrip(";").strip().strip("\t").strip("\"") for line in text.split("\n")]
			self.textEdit_output1.setText("\n".join(lines))

	def upper(self):  # 大写
		text = self.textEdit_input1.toPlainText()
		if text.strip():
			self.textEdit_output1.setText(text.rstrip().upper())

	def lower(self):  # 小写
		text = self.textEdit_input1.toPlainText()
		if text.strip():
			self.textEdit_output1.setText(text.rstrip().lower())

	def copy1(self):  # 复制结果
		text = self.textEdit_output1.toPlainText().strip()
		if text:
			pyperclip.copy(text)

	def clear1(self):  # 清空
		self.textEdit_input1.clear()
		self.textEdit_output1.clear()

	"""拓展功能"""
	def add(self):  # 新增
		row_new = self.tableWidget_input2.rowCount()  # 新增行行号

		'''下拉框声明及赋值'''
		combobox_connector = QComboBox()
		combobox_connector.addItems(self.CONNECTOR)

		'''添加至表单'''
		self.tableWidget_input2.insertRow(row_new)  # 新增一行
		self.tableWidget_input2.setCellWidget(row_new, 0, QCheckBox())  # 勾选列
		self.tableWidget_input2.setCellWidget(row_new, 2, combobox_connector)  # 赋值方式

	def delete(self):  # 删除
		for i in range(self.tableWidget_input2.rowCount() - 1, -1, -1):
			if self.tableWidget_input2.cellWidget(i, 0).isChecked():
				self.tableWidget_input2.removeRow(i)

	def generate_sql(self):  # 生成sql
		if self.tableWidget_input2.rowCount() > 0:
			lines1, lines2, lines3, lines4 = [], [], [], []

			for i in range(self.tableWidget_input2.rowCount()):
				if self.tableWidget_input2.item(i, 1):
					param = self.tableWidget_input2.item(i, 1).text().lower()
					param_u = param.upper()
					if param.strip():
						assignment = self.tableWidget_input2.cellWidget(i, 2).currentText()

						lines1.append(f"CString {param};")
						lines2.append(f"if (bcls_rec->Tables[0].Columns.Contains(\"{param_u}\"))")
						lines2.append("{")
						lines2.append(f"\t{param} = bcls_rec->Tables[0].Rows[0][\"{param_u}\"].ToString().Trim();")
						lines2.append("}")
						lines2.append(f"Log::Trace(\"\", \"\", \"传入值 {param} = [" + "{0}" + f"]\", {param});\n")
						lines3.append(f"if (bcls_rec->Tables[0].Columns.Contains(\"{param_u}\") && {param} != \"\")")

						line = "{\n\tsql_where += \" AND " + f"{param.upper()} "
						if "@" in self.comboBox_assignment.currentText():
							line += assignment.replace("param", f"@{param}")
						else:
							line += assignment.replace("param", f"'\" + {param} + \"'")

						lines3.append(line + "\";\n}")
						lines4.append(f"cmd.Parameters.Set(\"{param}\", {param});")

			if len(lines1):
				sql = f"/*{'-' * 32} 定义变量 {'-' * 32}*/\n" + "\n".join(lines1) +\
					f"\n\n/*{'-' * 32} 传入值 {'-' * 32}*/\n" + "\n".join(lines2) +\
					f"\n/*{'-' * 32} 拼接查询语句 {'-' * 32}*/\nCString sql_where = \"\";\n" + "\n".join(lines3) +\
					"\nLog::Trace(\"\", \"\", \"sql_where = [{0}]\", sql_where);"\
					f"\n\n/*{'-' * 32} 执行查询语句 {'-' * 32}*/\nsqlstr = \"SELECT * FROM  WHERE 1 = 1\" + sql_where;"\
					"\nLog::Trace(\"\", \"\", \"sqlstr = [{0}]\", sqlstr);\nCDbCommand cmd(sqlstr, conn);\n"
				if "@" in self.comboBox_assignment.currentText():
					sql += "\n".join(lines4) + "\n"
				if self.checkBox.isChecked():
					sql += "cmd.ExecuteQuery(bcls_ret->Tables[0], pageInfo.RecordFrom, pageInfo.PageSize);"
				else:
					sql += "cmd.ExecuteQuery(bcls_ret->Tables[0]);"
				sql += "\ncmd.Close();"

				if self.checkBox.isChecked():
					sql = "/*-------------------------------- 分页参数 --------------------------------*/"\
						"\nif (!bcls_rec->Tables.Contains(\"PAGE_INFO\"))\n{"\
						"\n\tstrcpy(s.msg, \"缺少分页参数表[PAGE_INFO]！\");\n\ts.flag = -1;\n\treturn -1;\n}"\
						"\nif (!bcls_rec->Tables[\"PAGE_INFO\"].Columns.Contains(\"RECORD_FROM\"))\n{"\
						"\n\tstrcpy(s.msg, \"缺少分页参数[RECORD_FROM]！\");\n\ts.flag = -1;\n\treturn -1;\n}"\
						"\nif (!bcls_rec->Tables[\"PAGE_INFO\"].Columns.Contains(\"PAGE_SIZE\"))\n{"\
						"\n\tstrcpy(s.msg, \"缺少分页参数[PAGE_SIZE]！\");\n\ts.flag = -1;\n\treturn -1;\n}"\
						"\n\nCPageInfo pageInfo;"\
						"\npageInfo.RecordFrom = bcls_rec->Tables[\"PAGE_INFO\"].Rows[0][\"RECORD_FROM\"]"\
						".ToDecimal().ToInt32();"\
						"\npageInfo.PageSize = bcls_rec->Tables[\"PAGE_INFO\"].Rows[0][\"PAGE_SIZE\"]"\
						".ToDecimal().ToInt32();"\
						"\nLog::Trace(\"\", \"\", \"分页参数 RECORD_FROM = [{0}]\", pageInfo.RecordFrom);"\
						"\nLog::Trace(\"\", \"\", \"分页参数 PAGE_SIZE = [{0}]\", pageInfo.PageSize);\n\n" + sql + "\n"\
						"\n/*-------------------------------- 分页信息 --------------------------------*/"\
						"\nCDbCommand cmd_count(\"SELECT COUNT(1) FROM (\" + sqlstr + \")\", conn);"\
						"\nbcls_ret->Tables.Add(\"PAGE_INFO\");"\
						"\nbcls_ret->Tables[\"PAGE_INFO\"].Clear();"\
						"\nbcls_ret->Tables[\"PAGE_INFO\"].Columns.Add(DT_DECIMAL, \"TOTAL_RECORD_COUNT\");"\
						"\nbcls_ret->Tables[\"PAGE_INFO\"].Rows.Add();"\
						"\nbcls_ret->Tables[\"PAGE_INFO\"].Rows[0][\"TOTAL_RECORD_COUNT\"]"\
						" = cmd_count.ExecuteScalar().ToInt32();"\
						"\ncmd_count.Close();"
				self.textEdit_output2.setText(sql)

	def copy2(self):  # 复制结果
		text = self.textEdit_output2.toPlainText().strip()
		if text:
			pyperclip.copy(text)

	def clear2(self):  # 清空
		self.tableWidget_input2.setRowCount(0)
		self.textEdit_output2.clear()


if __name__ == "__main__":
	QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)  # 自动适应高分辨率
	app = QApplication(sys.argv)  # 创建app（sys.argv是命令行参数列表）
	myWindow = Core()  # 初始化
	myWindow.show()  # 显示窗口控件
	sys.exit(app.exec_())  # 完整退出
