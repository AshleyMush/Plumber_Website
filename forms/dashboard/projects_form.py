from flask_wtf import FlaskForm

from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, URL


class ProjectForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    image = StringField('Image URL', validators=[URL(message="Please enter a valid URL for the project image.")])
    location = StringField('Location', validators=[DataRequired()])
    submit = SubmitField('Save')
