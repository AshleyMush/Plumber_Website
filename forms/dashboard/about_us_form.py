from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired, Optional, URL
from flask_wtf.file import FileAllowed


class AboutUsForm(FlaskForm):
    heading = StringField('Heading', validators=[DataRequired()])
    subheading = StringField('Subheading', validators=[DataRequired()])

    main_image_path = FileField(
        'Main Image',
        validators=[Optional(), FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Only image files are allowed.')]
    )
    image_one_path = FileField(
        'Image One',
        validators=[Optional(), FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Only image files are allowed.')]
    )
    image_two_path = FileField(
        'Image Two',
        validators=[Optional(), FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Only image files are allowed.')]
    )

    content_one_url = StringField(
        'Content One URL',
        validators=[Optional(), URL(message="Please enter a valid URL.")]
    )
    content_two_url = StringField(
        'Content Two URL',
        validators=[Optional(), URL(message="Please enter a valid URL.")]
    )
    content_three_url = StringField(
        'Content Three URL',
        validators=[Optional(), URL(message="Please enter a valid URL.")]
    )

    feature_one_heading = StringField('Feature One Heading', validators=[Optional()])
    feature_one_description = TextAreaField('Feature One Description', validators=[Optional()])
    feature_two_heading = StringField('Feature Two Heading', validators=[Optional()])
    feature_two_description = TextAreaField('Feature Two Description', validators=[Optional()])

    submit = SubmitField('Save Changes')
