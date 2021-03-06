from flask_wtf import FlaskForm
from wtforms import SubmitField, validators, IntegerField


class New_Assessment_Detail(FlaskForm):
    submit = SubmitField('Submit')


class Delete_Assessment(FlaskForm):
    submit = SubmitField('Delete')


class Submit_Assessment(FlaskForm):
    submit = SubmitField('Submit')

class Rate_Assessment_Form(FlaskForm):
    rating = IntegerField('Review(1-5)', validators=[validators.NumberRange(0, 5)])
    submit = SubmitField('Submit')