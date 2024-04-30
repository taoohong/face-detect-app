import os
import sqlite3

from database.model.building import Building

cur_dir = os.path.dirname(__file__)
class BuildingDB:
    def __init__(self):
        self.connection = sqlite3.connect(cur_dir + '/building.db')
        self.cursor = self.connection.cursor()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS building (
                    uid INTEGER PRIMARY KEY,
                    building_name TEXT NOT NULL UNIQUE,
                    location TEXT
                )''')
        self.connection.commit()

    def insert_building(self, building_name, location):
        self.cursor.execute("INSERT INTO building (building_name, location) VALUES (?, ?)",
                            (building_name, location,))
        self.connection.commit()
        return self.cursor.lastrowid

    def select_building(self, uid):
        result = self.cursor.execute("SELECT * FROM building WHERE uid = ?", (uid,))
        row = result.fetchone()
        b = Building(row[0], row[1], row[2])
        return b

    def select_by_building_name(self, building_name):
        result = self.cursor.execute("SELECT * FROM building WHERE building_name = ?", (building_name,))
        row = result.fetchone()
        b = Building(row[0], row[1], row[2])
        return b

    def select_all(self):
        self.cursor.execute("SELECT * FROM building")
        builds = []
        for row in self.cursor.fetchall():
            builds.append(Building(row[0], row[1], row[2]))
        return builds

    def delete_building(self, uid):
        self.cursor.execute("DELETE FROM building WHERE uid = ?", (uid,))
        self.connection.commit()

    def update_building(self, uid, building_name, location):
        self.cursor.execute("UPDATE FROM buildings SET building_name = ?, location= ? WHERE uid = ?",
                            (building_name, location, uid))
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()


if __name__ == '__main__':
    f = BuildingDB()
    f.create_table()
    f.insert_building("逸夫楼", "")
    f.insert_building("实验楼A", "")
    f.close()
