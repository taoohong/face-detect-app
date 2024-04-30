import os
import sqlite3

from database.model.course import Course

cur_dir = os.path.dirname(__file__)
class CourseDB:
    def __init__(self):
        self.connection = sqlite3.connect(cur_dir + '/course.db')
        self.cursor = self.connection.cursor()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS course (
                    uid INTEGER PRIMARY KEY,
                    course_name TEXT NOT NULL,
                    course_period TEXT NOT NULL,
                    hours INTEGER NOT NULL,
                    teacher TEXT NOT NULL
                )''')
        self.connection.commit()

    def insert_course(self, course_name, course_period, hours, teacher):
        self.cursor.execute("INSERT INTO course (course_name, course_period, hours, teacher) VALUES (?, ?, ?, ?)",
                            (course_name, course_period, hours, teacher,))
        self.connection.commit()
        return self.cursor.lastrowid

    def select_course(self, uid):
        result = self.cursor.execute("SELECT * FROM course WHERE uid = ?", (uid,))
        row = result.fetchone()
        c = Course(row[0], row[1], row[2], row[3], row[4])
        return c

    def select_by_cid(self, cid):
        result = self.cursor.execute("SELECT * FROM course WHERE cid = ?", (cid,))
        row = result.fetchone()
        c = Course(row[0], row[1], row[2], row[3], row[4])
        return c

    def select_all(self):
        self.cursor.execute("SELECT * FROM course")
        cs = []
        for row in self.cursor.fetchall():
            cs.append(Course(row[0], row[1], row[2], row[3], row[4]))
        return cs

    def delete_course(self, uid):
        self.cursor.execute("DELETE FROM course WHERE uid = ?", (uid,))
        self.connection.commit()

    def update_course(self, uid, course_name, course_period, hours, teacher):
        self.cursor.execute("UPDATE FROM course SET cid = ?, course_name = ?, course_period = ?, hours = ?, teacher = ?"
                            " WHERE uid = ?",(course_name, course_period, hours, teacher, uid))
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()


if __name__ == '__main__':
    f = CourseDB()
    f.create_table()
    f.insert_course("微积分上", "1-12周", 48, "teacher1")
    f.insert_course("微积分下", "12-24周", 48, "teacher1")
    f.insert_course("操作系统", "1-10周", 40, "teacher3")
    f.insert_course("Python", "1-10周", 40, "teacher4")
    f.insert_course("C/C++", "1-10周", 40, "teacher5")
    f.close()
