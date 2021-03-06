from project import db
from werkzeug.security import check_password_hash, generate_password_hash
from marshmallow import Schema, fields


class Admin(db.Model):
    __tablename__ = 'admin'

    id = db.Column(db.Integer,primary_key= True)
    fname = db.Column(db.String(40))
    lname = db.Column(db.String(40))
    uname = db.Column(db.String(40), unique=True)
    email = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(256))

    def __init__(self, fname, lname, uname, email, password):
        self.fname = fname
        self.lname = lname
        self.uname = uname
        self.email = email
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)


class AdminSchema(Schema):
    email = fields.Email()
    password = fields.Str()

class StudentSchema(Schema):
    id = fields.Int()
    fname = fields.Str()
    lname = fields.Str()
    uname = fields.Str()
    email = fields.Email()
    attempted = fields.Int()
    solved = fields.Int()
    score = fields.Int()

class ExaminerSchema(Schema):
    id = fields.Int()
    fname = fields.Str()
    lname = fields.Str()
    uname = fields.Str()
    email = fields.Email()

class CategorySchema(Schema):
    id = fields.Int()
    name = fields.Str()
    description = fields.Str()
    status = fields.Str()