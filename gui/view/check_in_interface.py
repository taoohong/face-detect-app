# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from time import sleep

import cv2
from PyQt5.QtCore import QTimer, QThread, pyqtSignal, QMutex, QWaitCondition
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QWidget, QDialog
from qfluentwidgets import MessageBox

from database.attendance_db import AttendanceDB
from view.UI_check_in_interface import Ui_checkInInterface
from face_recognition.face_recognizer import FaceRecognizer
from anti_spoofing.face_anti_spoof import FaceAntiSpoof
from gui import config


def can_check_in():
    warnings = ""
    if config.chosenSchedule is None:
        warnings = "请先设置考勤课程与时间"
    elif config.startTime == "" or config.endTime == "":
        warnings = "请先设置签到时间"
    elif datetime.strptime(config.startTime, '%Y-%m-%d %H:%M:%S') > datetime.now():
        warnings = "尚未开启签到"
    return warnings == "", warnings


class CheckInInterface(Ui_checkInInterface, QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

        self.face_recognizer = FaceRecognizer()
        self.face_anti_spoof = FaceAntiSpoof()
        self.attendanceDB = AttendanceDB()
        self.camera = None
        self.camera_started = False
        self.candidate_frames_cnt = 0
        self.candidate_student = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.process)
        self.cameraButt.clicked.connect(self.toggle_camera)

    def toggle_camera(self):
        if not self.camera_started:
            ret, warnings = can_check_in()
            if not ret:
                m = MessageBox("提示", warnings, self)
                m.cancelButton.hide()
                m.show()
                return
            if not self.camera:
                self.camera = cv2.VideoCapture(0)
            self.timer.start(50)  # 50 毫秒更新一次
            self.cameraButt.setText("关闭镜头")
        else:
            # 不关闭摄像头，快速进行下一次签到
            self.timer.stop()
            self.cameraButt.setText("点击签到")
            self.show_label.setImage('assets/check_in.png')
        self.camera_started = not self.camera_started
        self.candidate_frames_cnt = 0
        self.candidate_student = None

    def process(self):
        ret, frame = self.camera.read()
        if ret:
            frame, face_owner_list = self.face_recognizer.process(frame)
            frame, true_face = self.face_anti_spoof.detect(frame)
            h, w, ch = frame.shape
            q_img = QImage(frame.data, w, h, QImage.Format_RGB888)
            self.show_label.setPixmap(QPixmap.fromImage(q_img))
            if len(face_owner_list) > 0 and true_face:
                last = self.candidate_student
                self.candidate_student = face_owner_list[0]
                if last is None or self.candidate_student.sid != last.sid:
                    # 人物发生改变，计数清零
                    self.candidate_frames_cnt = 0
                self.candidate_frames_cnt += 1
                self.candidate_student = face_owner_list[0]
                # 连续8帧为同一人，且始终为活体，则签到成功
                if self.candidate_frames_cnt > 8:
                    self.check_in()
                    self.toggle_camera()
            # 非活体，计数清零
            elif not true_face:
                self.candidate_frames_cnt = 0
                self.candidate_student = None

    def check_in(self):
        end_time = datetime.strptime(config.endTime, '%Y-%m-%d %H:%M:%S')
        state = "ontime"
        if datetime.now() > end_time:
            state = "late"
        self.attendanceDB.insert_attendance(self.candidate_student.uid, config.chosenSchedule.uid,
                                            config.chosenClass.uid, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), state)
        m = MessageBox("提示", f"{self.candidate_student.name}同学签到成功！", self)
        m.cancelButton.hide()
        m.show()

    def hideEvent(self, a0):
        self.camera_started = False
        self.timer.stop()
        if self.camera is not None:
            self.camera.release()
            self.camera = None

    def closeEvent(self, a0):
        self.attendanceDB.close()
        a0.accept()