from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from wtforms import StringField,DecimalField, SubmitField,SelectField, TextAreaField, PasswordField, BooleanField
from wtforms.validators import DataRequired,NumberRange, URL, Email, Length, ValidationError, InputRequired, Optional, EqualTo
import re
from flask import flash
from wtforms import SelectMultipleField
from wtforms.widgets import ListWidget, CheckboxInput
from utils.validators import PhoneNumberValidator


class SocialMediaInfoForm(FlaskForm):
    hackerrank = StringField('HackerRank')
    github = StringField('Github')
    linkedin = StringField('LinkedIn')
    facebook = StringField('Facebook')
    instagram = StringField('Instagram')
    submit = SubmitField('Save')

class UpdateEmailForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Save')

class UpdatePhoneForm(FlaskForm):
    phone_number = StringField(
        'Phone Number',
        validators=[
            DataRequired(message="Phone number is required."),
            PhoneNumberValidator  # Use the custom validator
        ]
    )
    submit = SubmitField('Save')

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired(), Length(min=8)])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=8)])
    confirm_new_password = PasswordField('Confirm New Password', validators=[
        DataRequired(),
        EqualTo('new_password', message='Passwords must match.')
    ])
    submit = SubmitField('Change Password')

class AboutMeForm(FlaskForm):
    about = TextAreaField('About Me', validators=[DataRequired(), Length(max=1000)])
    submit = SubmitField('Save')


# ------ New forms for the portfolio section ------

class PlumberDetailsForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email(message="You seem to be missing @ or .",
                                                                   check_deliverability=True)])
    number = StringField(
        'Number',
        validators=[
            DataRequired(message="Phone number is required."),
            PhoneNumberValidator  # Use the custom validator
        ]
    )
    address = TextAreaField('Address', validators=[DataRequired()])
    submit = SubmitField('Save')

class ProjectForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    image = StringField('Image URL', validators=[URL(message="Please enter a valid URL for the project image.")])
    location = StringField('Location', validators=[DataRequired()])
    submit = SubmitField('Save')

class ReviewForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    review = TextAreaField('Review', validators=[DataRequired()])
    submit = SubmitField('Save')


