from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, FileField
from flask_ckeditor import CKEditorField

from wtforms.validators import DataRequired, Optional
from flask_wtf.file import FileAllowed

class JobsDoneForm(FlaskForm):
    name = StringField('Project Name', validators=[DataRequired()])
    main_image_path = FileField(
        'Main Image/ After Image',
        validators=[Optional(), FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')]
    )
    image_one_path = FileField('Before Image (optional)', validators=[Optional(), FileAllowed(['jpg', 'jpeg', 'png'])])
    image_two_path = FileField('Additional Image (optional)', validators=[Optional(), FileAllowed(['jpg', 'jpeg', 'png'])])
    location = StringField('Location', validators=[Optional()])

    description = CKEditorField('Project Description (optional)', validators=[Optional()])
    submit = SubmitField('Save Project')

class ReviewerForm(FlaskForm):
    name = StringField('Your Name', validators=[DataRequired()])
    review = TextAreaField('Review', validators=[DataRequired()])
    submit = SubmitField('Submit Review')
