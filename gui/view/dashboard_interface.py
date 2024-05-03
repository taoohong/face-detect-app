import logging
from datetime import datetime

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QWidget, QDialog, QListWidgetItem
from qfluentwidgets import Dialog, MessageBox, FluentIcon
from view.UI_dashboard_interface import Ui_dashboardInterface

from database.attendance_db import AttendanceDB, AttendanceState
from database.student_db import StudentDB
from gui import config


class DashboardInterface(Ui_dashboardInterface, QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setupUi(self)
        self.signed = []
        self.unsigned = []

        self.initFlip()
        self.refresh()

    def initFlip(self):
        self.flip.setItemSize(QSize(380, 200))
        self.flip.setFixedSize(QSize(760, 240))
        self.flip.setBorderRadius(15)
        self.flip.setSpacing(15)
        self.flip.addImages(['assets/flip1.png', 'assets/flip2.png', 'assets/flip1.png'])

    def initAttendance(self):
        if config.chosenClass is None:
            return
        studentDB = StudentDB()
        attendanceDB = AttendanceDB()
        students = studentDB.select_all_by_class(config.chosenClass.uid)
        attendances_raw = attendanceDB.select_attendance_by_class(config.chosenClass.uid, config.chosenSchedule.uid,
                                                              datetime.now().strftime('%Y-%m-%d'))
        attendances = [x[1] for x in attendances_raw]
        stats = [x[5] for x in attendances_raw]
        self.signed.clear()
        self.unsigned.clear()
        if not len(attendances):
            self.unsigned.extend(students)
        else:
            for student in students:
                for i in range(len(attendances)):
                    if student.uid == attendances[i]:
                        self.signed.append((student, stats[i]))
                    else:
                        self.unsigned.append(student)
        studentDB.close()
        attendanceDB.close()

    def initList(self):
        if len(self.signed) != self.signed_list.count() or len(self.unsigned) != self.unsigned_list.count():
            self.unsigned_list.clear()
            self.signed_list.clear()
            for s in self.unsigned:
                item = QListWidgetItem()
                item.setIcon(FluentIcon.EDUCATION.icon())
                item.setText(str(s))
                self.unsigned_list.addItem(item)
            self.unsigned_list.setItemAlignment(Qt.AlignCenter)
            self.unsigned_list.setSpacing(5)
            for (s, state) in self.signed:
                item = QListWidgetItem()
                item.setIcon(FluentIcon.EDUCATION.icon())
                info = str(s)
                if state == AttendanceState.LATE.value:
                    info += " 迟到⏰"
                elif state == AttendanceState.ONTIME.value:
                    info += " 准时👍"
                item.setText(info)
                self.signed_list.addItem(item)
            self.signed_list.setItemAlignment(Qt.AlignCenter)
            self.signed_list.setSpacing(5)

    def refresh(self):
        self.initAttendance()
        self.initList()

    def showEvent(self, event):
        self.refresh()
