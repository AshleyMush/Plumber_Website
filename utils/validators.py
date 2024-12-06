# validators.py

import phonenumbers
from wtforms.validators import ValidationError


def PhoneNumberValidator(form, field):
    try:
        # Replace 'GB' with your region code if you're not targeting the UK
        input_number = phonenumbers.parse(field.data, "GB")  # Explicitly set region to 'GB' for UK numbers

        # Check if the number is valid and is either a landline or mobile number
        number_type = phonenumbers.number_type(input_number)
        if not (phonenumbers.is_valid_number(input_number) and
                number_type in [
                    phonenumbers.PhoneNumberType.MOBILE,
                    phonenumbers.PhoneNumberType.FIXED_LINE,
                    phonenumbers.PhoneNumberType.FIXED_LINE_OR_MOBILE
                ]):
            raise ValidationError('Invalid phone number. Only mobile or landline numbers are allowed.')
    except phonenumbers.NumberParseException:
        raise ValidationError('Invalid phone number format.')
