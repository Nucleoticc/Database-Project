from project import db
from werkzeug.security import check_password_hash, generate_password_hash, safe_str_cmp
from flask_login import UserMixin


class Examiner(UserMixin, db.Model):
    __tablename__ = 'examiners'

    id = db.Column(db.Integer,primary_key= True)
    fname = db.Column(db.String(40))
    lname = db.Column(db.String(40))
    uname = db.Column(db.String(40), unique=True)
    email = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(256))
    profile_img = db.Column(db.String(64), nullable=False, default='default_profile.png')
    bio = db.Column(db.Text)
    role = "Examiner"

    def __init__(self, examiner_fname, examiner_lname, examiner_uname, examiner_email, examiner_password, examiner_bio):
        self.fname = examiner_fname
        self.lname = examiner_lname
        self.uname = examiner_uname
        self.email = examiner_email
        self.password = generate_password_hash(examiner_password)
        self.bio = examiner_bio
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_email(self, email):
        return safe_str_cmp(self.email, email)
