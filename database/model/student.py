class Student:
    def __init__(self, uid, sid, name, email, _class, gender, birth, phone):
        self.uid = uid
        self.sid = sid
        self.name = name
        self.email = email
        self._class = _class
        self.gender = gender
        self.birth = birth
        self.phone = phone

    def __repr__(self):
        return f"学生 {self.name}: [{self.sid}, {self._class.class_name}, {self.gender}]"

