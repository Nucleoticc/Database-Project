from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, validators

class NewCategoryRequest(FlaskForm):
    name = StringField('Name:', [validators.InputRequired()]) 
    desc = TextAreaField('Description', [validators.InputRequired()])
    submit = SubmitField('Submit')