from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from wtforms import StringField,DecimalField, SubmitField,SelectField, TextAreaField, PasswordField, BooleanField
from wtforms.validators import DataRequired,NumberRange, URL, Email, Length, ValidationError, InputRequired, Optional, EqualTo
import re
from flask import flash
from wtforms import SelectMultipleField
from wtforms.widgets import ListWidget, CheckboxInput
from utils.validators import PhoneNumberValidator



class ContactUSForm(FlaskForm):
    """
    Form for contact page
    """
    name = StringField(
        label='Name',
        validators=[DataRequired(), Length(max=64)],
        render_kw={"placeholder": "Full Name", "class": "form-control"}
    )

    email = StringField(
        label='Email',
        validators=[DataRequired(), Email(message="You seem to be missing @ or .", check_deliverability=True)],
        render_kw={"placeholder": "Email Address", "class": "form-control"}
    )

    phone = StringField(
        label='Phone',
        validators=[DataRequired(), Length(min=10, max=15, message="Please enter a valid phone number")],
        render_kw={"placeholder": "Phone Number", "class": "form-control"}
    )

    subject = SelectField(
        label='Subject',
        choices=[
            ('', 'How can we help you?'),  # Placeholder option
            ('gas_leakage', 'Gas Leakage'),
            ('plumbing', 'Plumbing'),
            ('drainage', 'Drainage'),
        ],
        validators=[DataRequired(message="Please select an option")],
        render_kw={"class": "form-control"}
    )

    message = TextAreaField(
        label='Message',
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter your message here", "class": "form-control", "rows": 5}
    )

    submit = SubmitField(
        label='Send Message',
        render_kw={"class": "btn btn-primary px-4 py-2"}
    )