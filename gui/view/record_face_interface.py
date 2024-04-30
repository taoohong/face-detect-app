import logging
import signal
import sqlite3

import cv2
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal, QObject, QWaitCondition, QMutex
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QDialog, QWidget
from qfluentwidgets import MessageBox
from view.UI_record_face_interface import Ui_recordFace
from face_recognition.face_register import FaceRegister
from face_recognition.operation import Operation


class RecordFaceInterface(Ui_recordFace, QWidget):
    def __init__(self, sid, signal, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowTitle("登记人脸")

        self.signal = signal
        self.sid = sid
        self.save_cnt = 0
        self.saved_face = 0
        self.camera = cv2.VideoCapture(0)
        self.face_register = FaceRegister()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.process)
        self.saveButt.clicked.connect(self.process_and_save)
        self.submitButt.clicked.connect(self.save_face)
        self.cancelButt.clicked.connect(self.close)
        self.timer.start(50)

    def process_and_save(self):
        self.save_cnt += 1
        self.saved_face = self.process_one_frame(Operation.SAVE)
        self.saveLabel.setText(f"已采集{self.save_cnt}份人脸数据")

    def process(self):
        self.process_one_frame()

    def process_one_frame(self, op=Operation.NONE):
        ret, frame = self.camera.read()
        if ret:
            frame, face = self.face_register.record(frame, op, self.sid)
            h, w, ch = frame.shape
            q_img = QImage(frame.data, w, h, QImage.Format_RGB888)
            self.cameraLabel.setPixmap(QPixmap.fromImage(q_img))
            if face is not None:
                h1, w1, ch1 = face.shape
                return QImage(face.data, w1, h1, QImage.Format_RGB888)
            else:
                return None

    def save_face(self):
        if self.face_register.face_registered(self.sid):
            m = MessageBox("警告⚠️", "人脸已登记，是否覆盖？", self)
            m.show()
            if m.exec_() == QDialog.Accepted:
                self.face_register.save_to_database(self.sid, True)
            else:
                m.close()
        else:
            self.face_register.save_to_database(self.sid)
        self.signal.emit(self.saved_face)
        self.close()

    def closeEvent(self, event):
        self.timer.stop()
        self.camera.release()
        event.accept()
