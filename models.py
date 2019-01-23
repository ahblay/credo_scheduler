from app import db
from sqlalchemy.dialects.postgresql import JSON, ARRAY

'''
class Result(db.Model):
    __tablename__ = 'results'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String())
    result_all = db.Column(JSON)
    result_no_stop_words = db.Column(JSON)

    def __init__(self, url, result_all, result_no_stop_words):
        self.url = url
        self.result_all = result_all
        self.result_no_stop_words = result_no_stop_words

    def __repr__(self):
        return '<id {}>'.format(self.id)
'''


class Teachers(db.Model):
    __tablename__ = 'teachers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    classes = db.Column(ARRAY(db.String))

    def __init__(self, id, name, classes):
        self.id = id
        self.name = name
        self.classes = classes

    def __repr__(self):
        return '<id {}>'.format(self.id)