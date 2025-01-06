from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired, URL, Optional, Regexp
from flask_wtf.file import FileAllowed, FileRequired

from flask_ckeditor import CKEditorField



# --- New Forms for the new models ---

class ServicesForm(FlaskForm):
    name =StringField('Name of the service you provide', validators=[DataRequired()])
    icon_class = StringField(
        'Icon Class (Bootstrap or Font Awesome)',
        validators=[
            Optional(),
            Regexp(
                r'^(fa-[a-z0-9\- ]+|bi-[a-z0-9\- ]+)$',
                message="Enter a valid Font Awesome (e.g., fa-solid fa-bath) or Bootstrap (e.g., bi-bootstrap-icon) class."
            )
        ]
    )

    main_image_path: FileField = FileField(
        'Upload  Service Page and Home Page Main Image',
        validators=[Optional(), FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Only image files are allowed.')]
    )
    home_page_card_text = TextAreaField('Home Page card text', validators=[DataRequired()])
    header_description = TextAreaField('Header Description', validators=[DataRequired()])
    image_one_path = FileField(
        'Upload  Service Page Feature One Image',
        validators=[Optional(), FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Only image files are allowed.')]
    )
    feature_heading_one = StringField('Feature One Heading', validators=[DataRequired()])
    feature_description_one = TextAreaField('Feature One Description', validators=[DataRequired()])
    image_two_path = FileField(
        'Upload  Service Page Feature Two Image',
        validators=[Optional(), FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Only image files are allowed.')]
    )
    feature_heading_two = StringField('Feature Two Heading', validators=[DataRequired()])
    feature_description_two = TextAreaField('Feature Two Description', validators=[DataRequired()])

    content_one_url = StringField('Youtube video or Image URL', validators=[URL(message="Please enter a valid URL for the content."),Optional()])

    submit = SubmitField('Save Changes')