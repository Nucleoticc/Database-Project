from project.students.models import Student
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, PasswordField, validators, TextAreaField


class SignUp(FlaskForm):
    fname = StringField('First Name:', [validators.InputRequired()]) 
    lname = StringField('Last Name:', [validators.InputRequired()]) 
    uname = StringField('Username:', [ validators.InputRequired() ])
    email = StringField('Email:', [validators.InputRequired(), validators.Email()]) 
    password = PasswordField('Password:',[validators.InputRequired(), validators.EqualTo('repassword', message='Passwords must match')])
    repassword = PasswordField('Confirm Password:')
    submit = SubmitField('Sign Up')
    
    def validate_email(self, email):
        student = Student.query.filter_by(email=email.data).first()
        if student is not None:
            raise validators.ValidationError('Please use a different email address.')


class LogIn(FlaskForm):
    email = StringField('Email:', [ validators.InputRequired(), validators.Email() ]) 
    password = PasswordField('Password', [ validators.InputRequired() ])
    submit = SubmitField('Log In')


class ChangeBasic(FlaskForm):
    firstname = StringField('First Name')
    lastname = StringField('Last Name')
    bio = TextAreaField('Bio')
    submit = SubmitField('Submit')


class ChangeDP(FlaskForm):
    picture = FileField('Update Profile Picture: ', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Update')


class ChangePassword(FlaskForm):
    oldpassword = PasswordField('Op', [ validators.InputRequired() ])
    newpassword = PasswordField('Np', [ validators.InputRequired() ])
    confirmpassword = PasswordField('Cp', [ validators.InputRequired() ])
    submit = SubmitField('Submit')


class Deactivate(FlaskForm):
    confirmpassword = PasswordField('confirm', [ validators.InputRequired() ])
    submit = SubmitField('Submit')