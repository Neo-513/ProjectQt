# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'exe_packer.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1263, 406)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton_impt = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_impt.setGeometry(QtCore.QRect(1000, 20, 111, 61))
        self.pushButton_impt.setObjectName("pushButton_impt")
        self.pushButton_pack = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_pack.setGeometry(QtCore.QRect(1130, 20, 111, 61))
        self.pushButton_pack.setObjectName("pushButton_pack")
        self.textEdit_log = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_log.setGeometry(QtCore.QRect(20, 100, 1221, 251))
        self.textEdit_log.setObjectName("textEdit_log")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1263, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_impt.setText(_translate("MainWindow", "导入"))
        self.pushButton_pack.setText(_translate("MainWindow", "打包"))
