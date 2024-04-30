class Course:
    def __init__(self, uid, course_name, course_period, hours, teacher):
        self.uid = uid
        self.course_name = course_name
        self.course_period = course_period
        self.hours = hours
        self.teacher = teacher

    def __repr__(self):
        return '<Course: {}>'.format(self.course_name)

    def __eq__(self, other):
        return self.uid == other.uid