import os
import sqlite3

from database.class_db import ClassDB
from database.model.student import Student

cur_dir = os.path.dirname(__file__)

class StudentDB:
    def __init__(self):
        self.connection = sqlite3.connect(cur_dir + '/students.db')
        self.cursor = self.connection.cursor()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS students (
                    uid INTEGER PRIMARY KEY,
                    sid TEXT NOT NULL UNIQUE,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE,
                    _class INTEGER NOT NULL,
                    gender TEXT NOT NULL,
                    birth DATE,
                    phone TEXT UNIQUE,
                    FOREIGN KEY (_class) REFERENCES class (uid)
                )''')
        self.connection.commit()

    def insert_student(self, sid, name, email, _class, gender, birth, phone):
        self.cursor.execute(
            "INSERT INTO students (sid, name, email,_class, gender, birth, phone) VALUES (?,?,?,?,?,?,?)",
            (sid, name, email, _class, gender, birth, phone))
        self.connection.commit()

    def select_student(self, student_id):
        result = self.cursor.execute("SELECT * FROM students WHERE uid = ?", (student_id,))
        row = result.fetchone()
        return Student(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])

    def select_student_by_sid(self, sid):
        result = self.cursor.execute("SELECT * FROM students WHERE sid = ?", (sid,))
        print(sid)
        row = result.fetchone()
        classDB = ClassDB()
        c = classDB.select_class(row[4])
        classDB.close()
        return Student(row[0], row[1], row[2], row[3], c, row[5], row[6], row[7])


    def select_all(self):
        self.cursor.execute("SELECT * FROM students")
        students = []
        classDB = ClassDB()
        for s in self.cursor.fetchall():
            students.append(Student(s[0], s[1], s[2], s[3], classDB.select_class(s[4]), s[5], s[6], s[7]))
        classDB.close()
        return students

    def select_all_by_class(self, class_id):
        self.cursor.execute("SELECT * FROM students WHERE _class = ?", (class_id,))
        students = []
        classDB = ClassDB()
        for s in self.cursor.fetchall():
            students.append(Student(s[0], s[1], s[2], s[3], classDB.select_class(s[4]), s[5], s[6], s[7]))
        classDB.close()
        return students

    def delete_student(self, student_id):
        self.cursor.execute("DELETE FROM students WHERE uid = ?", (student_id,))
        self.connection.commit()

    def update_student(self, student_id, sid, name, email, _class, gender, birth, phone):
        self.cursor.execute(
            "UPDATE FROM students SET sid = ?, name = ?, email = ?, _class = ?, gender = ?, birth = ?, phone = ? WHERE uid = ?",
            (sid, name, email, _class, gender, birth, phone, student_id))
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()


if __name__ == '__main__':
    s = StudentDB()
    s.create_table()
    s.insert_student("s202101", "张三", "example@qq.com", 1, "男", "2012-03-02", "18377028888")
    s.insert_student("s202102", "李四", "example1@qq.com", 1, "男", "2012-03-02", "1837702889")
    s.insert_student("s202103", "王五", "example2@qq.com", 1, "女", "2012-03-02", "1837702890")
    print(s.select_all())
    s.close()
