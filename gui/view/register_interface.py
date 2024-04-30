import logging

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QWidget, QDialog
from qfluentwidgets import Dialog, MessageBox
from view.UI_register_interface import Ui_registerInterface
from view.record_face_interface import RecordFaceInterface

from database.class_db import ClassDB
from database.student_db import StudentDB


def isIDValid(id):
    if id == '':
        return False
    # other requirements
    else:
        return True


class RegisterInterface(Ui_registerInterface, QWidget):
    update_avatar_signal = pyqtSignal(QImage)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.saved_face = None
        self.recordFaceInterface = None
        self.registerfaceButt.clicked.connect(self.recordFace)
        self.finishButt.clicked.connect(self.upload)
        self.update_avatar_signal.connect(self.update_avatar)

    def recordFace(self):
        sid = self.input_id.text()
        if isIDValid(sid):
            self.recordFaceInterface = RecordFaceInterface(sid, self.update_avatar_signal)
            self.recordFaceInterface.show()
        else:
            w = MessageBox('提示', '请检查ID', self)
            w.cancelButton.hide()
            w.show()

    def upload(self):
        sid = self.input_id.text()
        name = self.input_name.text()
        class_name = self.input_class.text()
        classDB = ClassDB()
        _class = classDB.select_by_class_name(class_name)
        email = self.input_email.text()
        phone = self.input_phone.text()
        checked_butt = self.input_gender.checkedButton()
        gender = "known"
        if checked_butt:
            gender = checked_butt.text()
        birth = self.input_birth.date.toString("yyyy-MM-dd")
        w = Dialog("确认上传",'', self)
        w.yesButton.setText("确认")
        w.cancelButton.setText("取消")
        if w.exec_() == QDialog.Accepted:
            if any(ele == "" for ele in [sid, name, class_name, email]):
                w = Dialog("警告", '请确定所有信息填写完成', self)
                w.yesButton.setText("确认")
                w.cancelButton.hide()
                w.show()
                return
            elif self.saved_face is None:
                w = Dialog("警告", '尚未登记人脸', self)
                w.yesButton.setText("确认")
                w.cancelButton.hide()
                w.show()
                return
            studentDB = StudentDB()
            studentDB.insert_student(sid, name, email, _class.uid, gender, birth, phone)
            classDB.close()
            studentDB.close()

    def update_avatar(self, avatar_img):
        self.saved_face = avatar_img
        self.label_avatar.setPixmap(QPixmap(avatar_img))
