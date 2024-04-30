import random

from PyQt5.QtWidgets import QWidget, QDialog
from qfluentwidgets import MessageBox
from view.UI_random_pick_interface import Ui_randomPickInterface

from database.student_db import StudentDB
from gui import config


class RandomPickInterface(Ui_randomPickInterface, QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.random_pick)

    def random_pick(self):
        if config.chosenClass is None:
            m = MessageBox("警告", "请先选择考勤班级", self)
            m.cancelButton.hide()
            m.show()
            return
        studentDB = StudentDB()
        ss = studentDB.select_all_by_class(config.chosenClass.uid)
        m = MessageBox("恭喜🎉", f"选中{ss[random.randint(0, len(ss) - 1)].name}同学!", self)
        m.cancelButton.hide()
        m.show()
        return

