# -*- coding: utf-8 -*-

# RandomPickInterface implementation generated from reading ui file '/Users/taohong/Programs/course-projects/face-detect/gui/pyqt_ui/random_pick_interface.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from qfluentwidgets import PushButton


class Ui_randomPickInterface(object):
    def setupUi(self, RandomPickInterface):
        RandomPickInterface.setObjectName("RandomPickInterface")
        RandomPickInterface.resize(850, 620)
        self.pushButton = PushButton(RandomPickInterface)
        self.pushButton.setGeometry(QtCore.QRect(350, 210, 113, 32))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(RandomPickInterface)
        QtCore.QMetaObject.connectSlotsByName(RandomPickInterface)

    def retranslateUi(self, RandomPickInterface):
        _translate = QtCore.QCoreApplication.translate
        RandomPickInterface.setWindowTitle(_translate("RandomPickInterface", "RandomPickInterface"))
        self.pushButton.setText(_translate("RandomPickInterface", "开始随机点名"))