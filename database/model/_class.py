class Class:
    def __init__(self, uid, class_name, colleage, grade, students):
        self.uid = uid
        self.class_name = class_name
        self.colleage = colleage
        self.grade = grade
        self.students = students

    def __repr__(self):
        return f'<Class {self.class_name} {self.grade} {self.colleage}>'

    def __eq__(self, other):
        return self.uid == other.uid