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




class CompanyDetailsForm(FlaskForm):
    name = StringField('Business Name', validators=[Optional()])
    logo = FileField(
        'Upload Business Logo',
        validators=[Optional(), FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Only image files are allowed.')]
    )
    address = StringField('Business Address', validators=[Optional()])
    motto = StringField('Motto', validators=[Optional()])
    about = TextAreaField('About', validators=[Optional()])
    openingHours = StringField('Opening Hours', validators=[Optional()])
    weekendHours = StringField('Weekend Hours', validators=[Optional()])
    show_location = BooleanField('Tick to Show Company Address and Map on Website (Default: No)', validators=[Optional()])
    submit = SubmitField('Save Changes')

    def validate_address(self, field):
        if self.show_location.data and not field.data:
            raise ValidationError('Address is required when "Show Location" is checked.')
