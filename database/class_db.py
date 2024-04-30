import os
import sqlite3

from database.model._class import Class

cur_dir = os.path.dirname(__file__)


class ClassDB:
    def __init__(self):
        self.connection = sqlite3.connect(cur_dir + '/class.db')
        self.cursor = self.connection.cursor()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS class (
                    uid INTEGER PRIMARY KEY,
                    class_name TEXT NOT NULL,
                    colleage TEXT NOT NULL,
                    grade TEXT NOT NULL,
                    students INTEGER NOT NULL
                )''')
        self.connection.commit()

    def insert_class(self, class_name, colleage, grade, students):
        self.cursor.execute("INSERT INTO class (class_name, colleage, grade, students) VALUES (?, ?, ?, ?)",
                            (class_name, colleage, grade, students,))
        self.connection.commit()
        return self.cursor.lastrowid

    def select_class(self, uid):
        result = self.cursor.execute("SELECT * FROM class WHERE uid = ?", (uid,))
        row = result.fetchone()
        c = Class(row[0], row[1], row[2], row[3], row[4])
        return c

    def select_by_class_name(self, class_name):
        result = self.cursor.execute("SELECT * FROM class WHERE class_name = ?", (class_name,))
        row = result.fetchone()
        c = Class(row[0], row[1], row[2], row[3], row[4])
        return c

    def select_all(self):
        self.cursor.execute("SELECT * FROM class")
        cs = []
        for row in self.cursor.fetchall():
            cs.append(Class(row[0], row[1], row[2], row[3], row[4]))
        return cs

    def delete_class(self, uid):
        self.cursor.execute("DELETE FROM class WHERE uid = ?", (uid,))
        self.connection.commit()

    def update_class(self, uid, class_name, colleage, grade, students):
        self.cursor.execute("UPDATE FROM class SET class_name = ?, colleage = ?, grade = ?, students = ? WHERE uid = ?",
                            (class_name, colleage, grade, students, uid))
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()


if __name__ == '__main__':
    f = ClassDB()
    f.create_table()
    f.insert_class("CS102", "计算机学院", "2018", 20)
    f.insert_class("CS103", "计算机学院", "2018", 21)
    f.insert_class("CS104", "计算机学院", "2018", 19)
    f.insert_class("EN104", "外国语学院", "2019", 19)
    f.insert_class("JP104", "外国语学院", "2019", 30)
    f.insert_class("SP104", "外国语学院", "2019", 23)
    f.close()
