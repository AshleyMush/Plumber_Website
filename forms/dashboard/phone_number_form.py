from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from utils.validators import PhoneNumberValidator


class UpdatePhoneForm(FlaskForm):
    phone_number = StringField(
        'Phone Number',
        validators=[
            DataRequired(message="Phone number is required. "),
            PhoneNumberValidator  # Use the custom validator
        ]
    )
    submit = SubmitField('Save')