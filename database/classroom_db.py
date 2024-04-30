import os
import sqlite3

from database.model.classroom import Classroom

cur_dir = os.path.dirname(__file__)



class ClassroomDB:
    def __init__(self):
        self.connection = sqlite3.connect(cur_dir + '/classroom.db')
        self.cursor = self.connection.cursor()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS classroom (
                    uid INTEGER PRIMARY KEY,
                    room_name INTEGER NOT NULL,
                    building_id INTEGER NOT NULL,
                    capacity INTEGER NOT NULL,
                    FOREIGN KEY (building_id) REFERENCES building (uid)
                )''')
        self.connection.commit()

    def insert_classroom(self, room_name, building_id, capacity):
        self.cursor.execute("INSERT INTO classroom (room_name, building_id, capacity) VALUES (?, ?, ?)",
                            (room_name, building_id, capacity,))
        self.connection.commit()
        return self.cursor.lastrowid

    def select_classroom(self, uid):
        result = self.cursor.execute("SELECT * FROM classroom WHERE uid = ?", (uid,))
        row = result.fetchone()
        c = Classroom(row[0], row[1], row[2], row[3])
        return c

    def select_by_room_name_and_building(self, room_name, building_id):
        result = self.cursor.execute("SELECT * FROM classroom WHERE room_name = ? and building_id = ?",
                                     (room_name, building_id))
        row = result.fetchone()
        c = Classroom(row[0], row[1], row[2], row[3])
        return c

    def select_all(self):
        self.cursor.execute("SELECT * FROM classroom")
        cs = []
        for row in self.cursor.fetchall():
            cs.append(Classroom(row[0], row[1], row[2], row[3]))
        return cs

    def select_all_by_building(self, building_id):
        self.cursor.execute("SELECT * FROM classroom WHERE building_id = ?", (building_id,))
        cs = []
        for row in self.cursor.fetchall():
            cs.append(Classroom(row[0], row[1], row[2], row[3]))
        return cs

    def delete_classroom(self, uid):
        self.cursor.execute("DELETE FROM classroom WHERE uid = ?", (uid,))
        self.connection.commit()

    def update_classroom(self, uid, room_name, building_id, capacity):
        self.cursor.execute("UPDATE FROM classrooms SET room_name = ?, building_id = ?, capacity = ? WHERE uid = ?",
                            (room_name, building_id, capacity, uid))
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()


if __name__ == '__main__':
    f = ClassroomDB()
    f.create_table()
    f.insert_classroom("101", 1, 50)
    f.insert_classroom("102", 1, 80)
    f.insert_classroom("103", 1, 40)
    f.insert_classroom("201", 1, 50)
    f.insert_classroom("202", 2, 80)
    f.insert_classroom("203", 2, 90)
    f.insert_classroom("204", 2, 100)
    f.close()
