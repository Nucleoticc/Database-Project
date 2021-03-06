from project import db


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(40), unique=True)
    description = db.Column(db.String(256))
    status = db.Column(db.String(10))

    def __init__(self, name, des, status):
        self.name = name
        self.description = des
        self.status = status
