from app import db
from sqlalchemy.dialects.postgresql import JSON, ARRAY


class Teachers(db.Model):
    __tablename__ = 'teachers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    classes = db.Column(ARRAY(db.String))
    primary = db.Column(db.Boolean(), default=True)

    def __init__(self, name, classes, primary):
        self.name = name
        self.classes = classes
        self.primary = primary

    def __repr__(self):
        return '<id {}>'.format(self.id)


class Classes(db.Model):
    __tablename__ = 'classes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    subject = db.Column(db.String())
    #year = db.Column(db.Integer())
    #teachers = db.Column(ARRAY(db.String))
    hours = db.Column(db.Integer())
    type = db.Column(db.String())
    code = db.Column(db.String())

    def __init__(self, name, subject, hours, type):
        self.name = name
        self.subject = subject
        #self.year = year
        #self.teachers = teachers
        self.hours = hours
        self.type = type
        self.code = name[0:3]

    def __repr__(self):
        return '<id {}>'.format(self.id)


class ClassPrefs(db.Model):
    __tablename__ = 'class_prefs'

    id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String())
    teacher_name = db.Column(db.String())
    pref = db.Column(db.Integer())

    def __init__(self, class_name, teacher_name, pref):
        self.class_name = class_name
        self.teacher_name = teacher_name
        self.pref = pref

    def __repr__(self):
        return '<id {}>'.format(self.id)