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
    heading = StringField('Main Heading ', validators=[DataRequired()])
    subheading  = StringField('Main Subheading ', validators=[DataRequired()])
    description = TextAreaField('Call to action description', validators=[Optional()])
    image_one = FileField('Upload image one', validators=[Optional(),
                                                            FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'mp4'],
                                                                        'Only image or video files are allowed.')])
    heading_two = StringField('Heading two', validators=[Optional()])
    subheading_two = StringField('Subheading two', validators=[Optional()])
    description_two = TextAreaField('Call to action description', validators=[Optional()])

    image_two = FileField('Upload image two', validators=[Optional(),
                                                            FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'mp4'],
                                                                        'Only image or video files are allowed.')])

    heading_three = StringField('Heading three', validators=[Optional()])
    subheading_three = StringField('Subheading three', validators=[Optional()])
    description_three = TextAreaField('Call to action description', validators=[Optional()])

    image_three = FileField('Upload image three', validators=[Optional(),
                                                              FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'mp4'],
                                                                          'Only image or video files are allowed.')])
    image_four = FileField('Upload image three', validators=[Optional(),
                                                             FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'mp4'],
                                                                         'Only image or video files are allowed.')])
    content_url_one = StringField('Image or Youtube Video URL ', validators=[Optional(), URL()])
    content_url_two = StringField('Image or Youtube Video URL ', validators=[Optional(), URL()])
    content_url_three = StringField('Image or Youtube Video URL ', validators=[Optional(), URL()])

    submit = SubmitField('Save Changes')