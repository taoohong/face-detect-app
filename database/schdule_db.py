import os
import sqlite3

from database.model.schedule import Schedule

cur_dir = os.path.dirname(__file__)


class ScheduleDB:
    def __init__(self):
        self.connection = sqlite3.connect(cur_dir + '/schedule.db')
        self.cursor = self.connection.cursor()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS schedule (
                    uid INTEGER PRIMARY KEY,
                    classroom_id INTEGER NOT NULL,
                    course_id INTEGER NOT NULL,
                    class_id INTEGER NOT NULL,
                    start_time TEXT NOT NULL,
                    end_time TEXT NOT NULL,
                    weekday TEXT NOT NULL,
                    FOREIGN KEY (classroom_id) REFERENCES classroom (uid),
                    FOREIGN KEY (course_id) REFERENCES course (uid),
                    FOREIGN KEY (class_id) REFERENCES class (uid)
                )''')
        self.connection.commit()

    def insert_schedule(self, classroom_id, course_id, class_id, start_time, end_time, weekday):
        self.cursor.execute("INSERT INTO schedule (classroom_id, course_id, class_id, start_time, end_time, weekday) "
                            "VALUES (?, ?, ?, ?, ?, ?)",
                            (classroom_id, course_id, class_id, start_time, end_time, weekday))
        self.connection.commit()
        return self.cursor.lastrowid

    def select_schedule(self, uid):
        result = self.cursor.execute("SELECT * FROM schedule WHERE uid = ?", (uid,))
        row = result.fetchone()
        s = Schedule(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
        return s

    def select_all(self):
        self.cursor.execute("SELECT * FROM schedule")
        ss = []
        for row in self.cursor.fetchall():
            ss.append(Schedule(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
        return ss

    def select_all_by(self, classroom_id=None, course_id=None, class_id=None, start_time=None, end_time=None, weekday=None):
        query = f"SELECT * FROM schedule WHERE "
        conditions = []
        if classroom_id is not None:
            conditions.append(classroom_id)
            query += "classroom_id = ?"
            query += " AND "
        if course_id is not None:
            conditions.append(course_id)
            query += "course_id = ?"
            query += " AND "
        if class_id is not None:
            conditions.append(class_id)
            query += "class_id = ?"
            query += " AND "
        if start_time is not None:
            conditions.append(start_time)
            query += "start_time = ?"
            query += " AND "
        if end_time is not None:
            conditions.append(end_time)
            query += "end_time = ?"
            query += " AND "
        if weekday is not None:
            conditions.append(weekday)
            query += "weekday = ?"
        query = query.strip()
        if query.endswith("AND"):
                query = query[:-3]
        self.cursor.execute(query, tuple(conditions))
        ss = []
        for row in self.cursor.fetchall():
            ss.append(Schedule(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
        return ss

    def delete_schedule(self, uid):
        self.cursor.execute("DELETE FROM schedule WHERE uid = ?", (uid,))
        self.connection.commit()

    def update_schedule(self, uid, classroom_id, course_id, class_id, start_time, end_time, weekday):
        self.cursor.execute("UPDATE FROM schedules SET classroom_id = ?, course_id = ?, class_id = ?, "
                            "start_time = ?, end_time = ?, weekday = ? WHERE uid = ?",
                            (classroom_id, course_id, class_id, start_time, end_time, weekday, uid))
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()


if __name__ == '__main__':
    f = ScheduleDB()
    f.create_table()
    f.insert_schedule(1, 2,3, "08:30:00", "11:30:00", "Monday")
    f.insert_schedule(2, 4, 2, "14:00:00", "15:30:00", "Thursday")
    f.insert_schedule(3, 1, 4, "14:00:00", "15:30:00", "Friday")
    f.insert_schedule(1, 3, 1, "18:30:00", "20:30:00", "Tuesday")
    f.insert_schedule(4, 5, 3, "18:30:00", "20:30:00", "Wednesday")
    f.close()
