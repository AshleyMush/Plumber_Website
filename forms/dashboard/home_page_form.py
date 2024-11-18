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
    image_one = FileField('1st Image or Video', validators=[Optional(),
                                                            FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'mp4'],
                                                                        'Only image or video files are allowed.')])
    image_two = FileField('2nd Image or Video', validators=[Optional(),
                                                            FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'mp4'],
                                                                        'Only image or video files are allowed.')])
    image_three = FileField('3rd Image or Video', validators=[Optional(),
                                                              FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'mp4'],
                                                                          'Only image or video files are allowed.')])
    image_four = FileField('4th Image or Video', validators=[Optional(),
                                                             FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'mp4'],
                                                                         'Only image or video files are allowed.')])

    submit = SubmitField('Save Changes')