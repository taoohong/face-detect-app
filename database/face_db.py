import os
import sqlite3

cur_dir = os.path.dirname(__file__)
class FaceDB:
    def __init__(self):
        self.connection = sqlite3.connect(cur_dir + '/faces.db')
        self.cursor = self.connection.cursor()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS faces (
                    uid INTEGER PRIMARY KEY,
                    face_feature TEXT NOT NULL,
                    owner TEXT NOT NULL UNIQUE,
                    FOREIGN KEY (owner) REFERENCES students (sid)
                )''')
        self.connection.commit()

    def insert_face(self, feature, owner_id):
        self.cursor.execute("INSERT INTO faces (face_feature, owner) VALUES (?, ?)", (feature, owner_id,))
        self.connection.commit()
        return self.cursor.lastrowid

    def select_face(self, face_id):
        result = self.cursor.execute("SELECT * FROM faces WHERE uid = ?", (face_id,))
        row = result.fetchone()
        return row

    def select_by_owner(self, owner_id):
        result = self.cursor.execute("SELECT * FROM faces WHERE owner = ?", (owner_id,))
        row = result.fetchone()
        return row

    def select_all(self):
        self.cursor.execute("SELECT * FROM faces")
        return self.cursor.fetchall()

    def delete_face(self, face_id):
        self.cursor.execute("DELETE FROM faces WHERE uid = ?", (face_id,))
        self.connection.commit()

    def delete_face_by_owner(self, owner_id):
        self.cursor.execute("DELETE FROM faces WHERE owner = ?", (owner_id,))
        self.connection.commit()

    def update_face(self, face_id, feature, owner_id):
        self.cursor.execute("UPDATE FROM faces SET face_feature = ?, owner = ? WHERE uid = ?",
                            (feature, owner_id, face_id))
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()


if __name__ == '__main__':
    f = FaceDB()
    f.create_table()
    f.close()
