# -*- coding: utf-8 -*-

# Form implementation generated from reading gui file '/Users/taohong/Programs/course-projects/face-detect/gui/pyqt_ui/check_in_interface.gui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from qfluentwidgets import ImageLabel, PushButton


class Ui_checkInInterface(object):
    def setupUi(self, checkInInterface):
        checkInInterface.setObjectName("checkInInterface")
        checkInInterface.setEnabled(True)
        checkInInterface.resize(850, 620)
        self.verticalLayoutWidget = QtWidgets.QWidget(checkInInterface)
        self.verticalLayoutWidget.resize(850, 620)
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")

        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout_2.setContentsMargins(20, 10, 20, 10)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.show_label = ImageLabel(image='assets/check_in.png', parent=self.verticalLayoutWidget)
        self.show_label.resize(800, 500)
        self.show_label.setBorderRadius(8, 8, 8, 8)
        self.show_label.setAlignment(QtCore.Qt.AlignCenter)
        self.show_label.setObjectName("show_label")
        self.verticalLayout_2.addWidget(self.show_label, 0, QtCore.Qt.AlignCenter)

        self.cameraButt = PushButton(self.verticalLayoutWidget)
        self.cameraButt.setObjectName("cameraButt")
        self.cameraButt.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout_2.addWidget(self.cameraButt, 0, QtCore.Qt.AlignHCenter)

        self.retranslateUi(checkInInterface)
        QtCore.QMetaObject.connectSlotsByName(checkInInterface)

    def retranslateUi(self, checkInInterface):
        _translate = QtCore.QCoreApplication.translate
        checkInInterface.setWindowTitle(_translate("checkInInterface", "Form"))
        self.show_label.setText(_translate("checkInInterface", "TextLabel"))
        self.cameraButt.setText(_translate("checkInInterface", "点击签到"))