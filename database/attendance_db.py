import enum
import os
import sqlite3
from enum import Enum

cur_dir = os.path.dirname(__file__)


class AttendanceState(Enum):
    ONTIME = "ontime"
    LATE = "late"
    ABSENCE = "absence"


class AttendanceDB:
    def __init__(self):
        self.connection = sqlite3.connect(cur_dir + '/attendance.db')
        self.cursor = self.connection.cursor()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS attendance (
                    uid INTEGER PRIMARY KEY,
                    student_id INTEGER NOT NULL,
                    schedule_id INTEGER NOT NULL,
                    class_id INTERGER NOT NULL,
                    date TEXT NOT NULL,
                    state TEXT NOT NULL,
                    FOREIGN KEY (student_id) REFERENCES student(uid),
                    FOREIGN KEY (schedule_id) REFERENCES schedule(uid),
                    FOREIGN KEY(class_id) REFERENCES class(uid)
                )''')
        self.connection.commit()

    def insert_attendance(self, student_id, schedule_id, class_id, date, state):
        self.cursor.execute(
            "INSERT INTO attendance (student_id, schedule_id, class_id, date, state) VALUES (?, ?, ?, ?, ?)",
            (student_id, schedule_id, class_id, date, state))
        self.connection.commit()
        return self.cursor.lastrowid

    def select_attendance(self, uid):
        result = self.cursor.execute("SELECT * FROM attendance WHERE uid = ?", (uid,))
        row = result.fetchone()
        return row

    def select_attendance_by_class(self, class_id, schedule_id, date):
        result = self.cursor.execute("SELECT * FROM attendance WHERE class_id = ? AND schedule_id = ? AND date LIKE ?",
                                     (class_id, schedule_id, date + " " + '%'))
        return result.fetchall()

    def select_all(self):
        self.cursor.execute("SELECT * FROM attendance")
        return self.cursor.fetchall()

    def delete_attendance(self, uid):
        self.cursor.execute("DELETE FROM attendance WHERE uid = ?", (uid,))
        self.connection.commit()

    def update_attendance(self, uid, student_id, schedule_id, class_id, date, state):
        self.cursor.execute(
            "UPDATE FROM attendances SET student_id = ?, schedule_id= ?, class_id, date = ?, state = ? WHERE uid = ?",
            (student_id, schedule_id, class_id, date, state, uid))
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()


if __name__ == '__main__':
    f = AttendanceDB()
    f.create_table()
    f.close()
