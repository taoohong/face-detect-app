class Classroom:
    def __init__(self, uid, name, building, capacity):
        self.uid = uid
        self.name = name
        self.building = building
        self.capacity = capacity

    def __repr__(self):
        return ("<Classroom(uid='%s', name='%s', building='%s', capacity='%s')>" %
                (self.uid, self.name, self.building, self.capacity))