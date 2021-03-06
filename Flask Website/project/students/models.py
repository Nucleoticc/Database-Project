from project import db
from werkzeug.security import check_password_hash, generate_password_hash, safe_str_cmp
from flask_login import UserMixin


class Student(UserMixin, db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer,primary_key= True)
    fname = db.Column(db.String(40))
    lname = db.Column(db.String(40))
    uname = db.Column(db.String(40), unique=True)
    email = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(256))
    attempted = db.Column(db.Integer)
    solved = db.Column(db.Integer)
    score = db.Column(db.Integer)
    profile_img = db.Column(db.String(64), nullable=False, default='default_profile.png')
    bio = db.Column(db.String(1024))
    role = "Student"

    def __init__(self, student_fname, student_lname, student_uname, student_email, student_password,student_attempted, student_solved, student_score, student_bio):
        self.fname = student_fname
        self.lname = student_lname
        self.uname = student_uname
        self.email = student_email
        self.password = generate_password_hash(student_password)
        self.attempted = student_attempted
        self.solved = student_solved
        self.score = student_score
        self.bio = student_bio
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_email(self, email):
        return safe_str_cmp(self.email, email)
