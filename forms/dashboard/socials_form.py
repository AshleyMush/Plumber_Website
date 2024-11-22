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



class SocialsForm(FlaskForm):
    instagram = StringField('Instagram URL', validators=[Optional(), URL()])
    whatsapp = StringField('WhatsApp Number', validators=[Optional()])
    youtube = StringField('YouTube Channel URL', validators=[Optional(), URL()])
    facebook = StringField('Facebook URL', validators=[Optional(), URL()])
    threads = StringField('Threads URL', validators=[Optional(), URL()])
    x = StringField('X (Twitter) URL', validators=[Optional(), URL()])
    submit = SubmitField('Save Changes')