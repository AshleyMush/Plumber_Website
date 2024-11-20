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


class AccreditationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    image = FileField(
        'Upload Image',
        validators=[Optional(), FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Only image files are allowed.')]
    )
    description = TextAreaField('Description of qualification', validators=[Optional()])
    submit = SubmitField('Save')