from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from wtforms import StringField,DecimalField, SubmitField,SelectField, TextAreaField, PasswordField, BooleanField
from wtforms.validators import DataRequired,NumberRange, URL, Email, Length, ValidationError, InputRequired, Optional, EqualTo
import re
from flask import flash
from wtforms import SelectMultipleField
from wtforms.widgets import ListWidget, CheckboxInput
from utils.validators import PhoneNumberValidator



class ContactForm(FlaskForm):
    """
    Form for contact page
    """
    name = StringField(label='Name', validators=[DataRequired(), Length(max=64)],
                       render_kw={"placeholder": "Name",
                                  "class": "contact-form"})

    email = StringField(label='Email', validators=[DataRequired(), Email(message="You seem to be missing @ or .",
                                                                         check_deliverability=True)])


    message = TextAreaField(label='Message', validators=[DataRequired()],
                            render_kw={"placeholder": "Enter your message here",
                                       "class": "col-12"})

    submit = SubmitField(label='Send Message', render_kw={"class": "btn btn-dark col-12",
                                                          "id": "contact_submit_btn"})
