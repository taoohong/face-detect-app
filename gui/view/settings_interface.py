import logging
from datetime import datetime

from PyQt5.QtWidgets import QDialog, QWidget
from view.UI_settings_interface import Ui_settingsInterface

from database.building_db import BuildingDB
from database.class_db import ClassDB
from database.classroom_db import ClassroomDB
from database.course_db import CourseDB
from database.schdule_db import ScheduleDB
from gui import config


class SettingsInterface(Ui_settingsInterface, QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.buildingDB = BuildingDB()
        self.classroomDB = ClassroomDB()
        self.courseDB = CourseDB()
        self.classDB = ClassDB()
        self.scheduleDB = ScheduleDB()
        self.buildings = []
        self.classrooms = []
        self.classes = []
        self.courses = []
        self.schedules = []
        self.initComboBox()
        config.chosenClass = None
        config.chosenBuilding = None
        config.chosenClassRoom = None
        config.chosenCourse = None
        config.chosenSchedule = None
        self.buildingComboBox.currentIndexChanged.connect(self.updateBuildingComboBox)
        self.classroomComboBox.currentIndexChanged.connect(self.updateClassroomComboBox)
        self.classComboBox.currentIndexChanged.connect(self.updateClassComboBox)
        self.courseComboBox.currentIndexChanged.connect(self.updateCourseComboBox)
        self.timeEdit.dateTimeChanged.connect(self.updateStartTime)
        self.timeEdit_2.dateTimeChanged.connect(self.updateEndTime)

    def initComboBox(self):
        self.buildings = self.buildingDB.select_all()
        for b in self.buildings:
            self.buildingComboBox.addItem(b.name)
        self.updateBuildingComboBox()

    def updateBuildingComboBox(self):
        if len(self.classrooms):
            self.classrooms.clear()
            self.classroomComboBox.clear()
        config.chosenBuilding = self.buildings[self.buildingComboBox.currentIndex()]
        self.classrooms = self.classroomDB.select_all_by_building(config.chosenBuilding.uid)
        for r in self.classrooms:
            self.classroomComboBox.addItem(str(r.name))
        self.updateClassroomComboBox()

    def updateClassroomComboBox(self):
        if len(self.classrooms):
            self.classes.clear()
            self.classComboBox.clear()
        if 0 <= self.classroomComboBox.currentIndex() < len(self.classrooms):
            config.chosenClassroom = self.classrooms[self.classroomComboBox.currentIndex()]
            self.schedules = self.scheduleDB.select_all_by(classroom_id=config.chosenClassroom.uid)
            for s in self.schedules:
                c = self.classDB.select_class(s.class_id)
                if c not in self.classes:
                    self.classes.append(c)
                    self.classComboBox.addItem(c.class_name)
            self.updateClassComboBox()

    def updateClassComboBox(self):
        if len(self.courses):
            self.courses.clear()
            self.courseComboBox.clear()
        if 0 <= self.classComboBox.currentIndex() < len(self.classes):
            config.chosenClass = self.classes[self.classComboBox.currentIndex()]
            self.schedules = self.scheduleDB.select_all_by(classroom_id=config.chosenClassroom.uid,
                                                           class_id=config.chosenClass.uid)
            for s in self.schedules:
                c = self.courseDB.select_course(s.course_id)
                if c not in self.courses:
                    self.courses.append(c)
                    self.courseComboBox.addItem(c.course_name)
            self.updateCourseComboBox()

    def updateCourseComboBox(self):
        if 0 <= self.courseComboBox.currentIndex() < len(self.courses):
            config.chosenCourse = self.courses[self.courseComboBox.currentIndex()]
            # 此处默认选择第一项作为具体签到课程
            # 后续可根据上课时间，上课教师等进一步细化选择
            config.chosenSchedule = self.scheduleDB.select_all_by(course_id=config.chosenCourse.uid, class_id=config.chosenClass.uid,
                                                                classroom_id=config.chosenClassroom.uid)[0]
            self.schedule_info.setText(f"课程名称-{config.chosenCourse.course_name}, 教师-{config.chosenCourse.teacher}, "
                                        f"课程时间-{config.chosenSchedule.start_time} 至 {config.chosenSchedule.end_time}")
        else:
            self.schedule_info.setText("请先选择课程")
    def updateStartTime(self):
        time = self.timeEdit.time().toString()
        config.startTime = datetime.now().strftime("%Y-%m-%d") + " " + time


    def updateEndTime(self):
        time = self.timeEdit_2.time().toString()
        config.endTime = datetime.now().strftime("%Y-%m-%d") + " " + time

    def closeEvent(self, a0):
        self.buildingDB.close()
        self.classroomDB.close()
        self.courseDB.close()
        self.scheduleDB.close()
