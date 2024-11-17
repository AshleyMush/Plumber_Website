from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from wtforms import StringField,FileField,DecimalField, SubmitField,SelectField, TextAreaField, PasswordField, BooleanField
from wtforms.validators import DataRequired,NumberRange, URL, Email, Length, ValidationError, InputRequired, Optional, EqualTo
from flask_wtf.file import FileAllowed, FileRequired
import re
from flask import flash
from wtforms import SelectMultipleField
from wtforms.widgets import ListWidget, CheckboxInput
from utils.validators import PhoneNumberValidator



class HomePageContentForm(FlaskForm):
    heading = StringField('Heading', validators=[DataRequired()])
    subheading  = StringField('Subheading')
    description = TextAreaField('Call to action description', validators=[Optional()])
    image_one = StringField('1st Image or video URL', validators=[URL(message="Please enter a valid URL for the feature one image/video.")])
    image_two = StringField('2nd Image or video URL', validators=[URL(message="Please enter a valid URL for the feature two image/video.")])
    image_three = StringField('3rd Image or video URL', validators=[URL(message="Please enter a valid URL for the feature three image/video.")])
    image_four = StringField('4th Image or video URL', validators=[URL(message="Please enter a valid URL for the feature four image/video.")])

    submit = SubmitField('Save Changes')