# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'game2048.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(381, 440)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_score = QtWidgets.QLabel(self.centralwidget)
        self.label_score.setGeometry(QtCore.QRect(30, 20, 111, 21))
        self.label_score.setObjectName("label_score")
        self.pushButton_start = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_start.setGeometry(QtCore.QRect(270, 20, 81, 28))
        self.pushButton_start.setObjectName("pushButton_start")
        self.label_00 = QtWidgets.QLabel(self.centralwidget)
        self.label_00.setGeometry(QtCore.QRect(30, 60, 81, 81))
        self.label_00.setObjectName("label_00")
        self.label_01 = QtWidgets.QLabel(self.centralwidget)
        self.label_01.setGeometry(QtCore.QRect(110, 60, 81, 81))
        self.label_01.setObjectName("label_01")
        self.label_03 = QtWidgets.QLabel(self.centralwidget)
        self.label_03.setGeometry(QtCore.QRect(270, 60, 81, 81))
        self.label_03.setObjectName("label_03")
        self.label_02 = QtWidgets.QLabel(self.centralwidget)
        self.label_02.setGeometry(QtCore.QRect(190, 60, 81, 81))
        self.label_02.setObjectName("label_02")
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(110, 140, 81, 81))
        self.label_11.setObjectName("label_11")
        self.label_13 = QtWidgets.QLabel(self.centralwidget)
        self.label_13.setGeometry(QtCore.QRect(270, 140, 81, 81))
        self.label_13.setObjectName("label_13")
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setGeometry(QtCore.QRect(190, 140, 81, 81))
        self.label_12.setObjectName("label_12")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(30, 140, 81, 81))
        self.label_10.setObjectName("label_10")
        self.label_21 = QtWidgets.QLabel(self.centralwidget)
        self.label_21.setGeometry(QtCore.QRect(110, 220, 81, 81))
        self.label_21.setObjectName("label_21")
        self.label_23 = QtWidgets.QLabel(self.centralwidget)
        self.label_23.setGeometry(QtCore.QRect(270, 220, 81, 81))
        self.label_23.setObjectName("label_23")
        self.label_30 = QtWidgets.QLabel(self.centralwidget)
        self.label_30.setGeometry(QtCore.QRect(30, 300, 81, 81))
        self.label_30.setObjectName("label_30")
        self.label_31 = QtWidgets.QLabel(self.centralwidget)
        self.label_31.setGeometry(QtCore.QRect(110, 300, 81, 81))
        self.label_31.setObjectName("label_31")
        self.label_22 = QtWidgets.QLabel(self.centralwidget)
        self.label_22.setGeometry(QtCore.QRect(190, 220, 81, 81))
        self.label_22.setObjectName("label_22")
        self.label_32 = QtWidgets.QLabel(self.centralwidget)
        self.label_32.setGeometry(QtCore.QRect(190, 300, 81, 81))
        self.label_32.setObjectName("label_32")
        self.label_33 = QtWidgets.QLabel(self.centralwidget)
        self.label_33.setGeometry(QtCore.QRect(270, 300, 81, 81))
        self.label_33.setObjectName("label_33")
        self.label_20 = QtWidgets.QLabel(self.centralwidget)
        self.label_20.setGeometry(QtCore.QRect(30, 220, 81, 81))
        self.label_20.setObjectName("label_20")
        self.label_step = QtWidgets.QLabel(self.centralwidget)
        self.label_step.setGeometry(QtCore.QRect(150, 20, 91, 21))
        self.label_step.setObjectName("label_step")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 381, 26))
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
        self.label_score.setText(_translate("MainWindow", "SCORE: 0"))
        self.pushButton_start.setText(_translate("MainWindow", "START"))
        self.label_00.setText(_translate("MainWindow", "TextLabel"))
        self.label_01.setText(_translate("MainWindow", "TextLabel"))
        self.label_03.setText(_translate("MainWindow", "TextLabel"))
        self.label_02.setText(_translate("MainWindow", "TextLabel"))
        self.label_11.setText(_translate("MainWindow", "TextLabel"))
        self.label_13.setText(_translate("MainWindow", "TextLabel"))
        self.label_12.setText(_translate("MainWindow", "TextLabel"))
        self.label_10.setText(_translate("MainWindow", "TextLabel"))
        self.label_21.setText(_translate("MainWindow", "TextLabel"))
        self.label_23.setText(_translate("MainWindow", "TextLabel"))
        self.label_30.setText(_translate("MainWindow", "TextLabel"))
        self.label_31.setText(_translate("MainWindow", "TextLabel"))
        self.label_22.setText(_translate("MainWindow", "TextLabel"))
        self.label_32.setText(_translate("MainWindow", "TextLabel"))
        self.label_33.setText(_translate("MainWindow", "TextLabel"))
        self.label_20.setText(_translate("MainWindow", "TextLabel"))
        self.label_step.setText(_translate("MainWindow", "STEP: 0"))
