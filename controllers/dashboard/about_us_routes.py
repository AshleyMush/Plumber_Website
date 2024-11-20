from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required
from models import db, AboutUsPageContent
from forms import AboutUsForm
from . import dashboard_bp
from utils.decorators import roles_required
from werkzeug.utils import secure_filename
import os

# Configure Upload Folder
UPLOAD_FOLDER = 'static/uploads/about_us'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)



@dashboard_bp.app_context_processor
def inject_home_content_status():
    about_us_exists = AboutUsPageContent.query.count() > 0
    return {'about_us_exists': about_us_exists}



@dashboard_bp.route('/add-about-us-content', methods=['GET', 'POST'])
@roles_required('Admin')
@login_required
def add_about_us_content():
    """
    Add About Us page content to the database with image uploading capabilities.
    """
    form = AboutUsForm()
    if form.validate_on_submit():
        try:
            # Handle file uploads for images
            uploaded_images = {}
            for image_field in ['image_one', 'image_two']:
                image_data = getattr(form, image_field).data
                if image_data:
                    filename = secure_filename(image_data.filename)
                    relative_path = os.path.join('uploads', 'about_us', filename).replace("\\", "/")
                    full_path = os.path.join('static', relative_path)
                    image_data.save(full_path)
                    uploaded_images[image_field] = relative_path  # Save relative path for each image

            # Add new content to the database
            new_about_us_content = AboutUsPageContent(
                heading=form.heading.data,
                subheading=form.subheading.data,
                description=form.description.data,
                image_one=uploaded_images.get('image_one'),
                image_two=uploaded_images.get('image_two'),
                content_url_one=form.content_url_one.data,
                content_url_two=form.content_url_two.data,
            )
            db.session.add(new_about_us_content)
            db.session.commit()
            flash('About Us Page Content added successfully', 'success')
            return redirect(url_for('dashboard_bp.update_about_us_page'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
    return render_template('dashboard/about_us/add-about-us-content.html', form=form)


@dashboard_bp.route('/update-about-us-page', methods=['GET', 'POST'])
@roles_required('Admin')
@login_required
def update_about_us_page():
    """
    Update About Us page content with image uploading capabilities.
    """
    about_us_content_to_update = AboutUsPageContent.query.first()
    if not about_us_content_to_update:
        flash("No About Us content found to update. Please add content first.", 'warning')
        return redirect(url_for('dashboard_bp.add_about_us_content'))

    form = AboutUsForm()

    # Pre-fill form with existing data on GET requests
    if request.method == 'GET':
        form.heading.data = about_us_content_to_update.heading
        form.subheading.data = about_us_content_to_update.subheading
        form.description.data = about_us_content_to_update.description
        form.content_url_one.data = about_us_content_to_update.content_url_one
        form.content_url_two.data = about_us_content_to_update.content_url_two
        form.image_one.data = None
        form.image_two.data = None

    if form.validate_on_submit():
        try:
            # Update text fields
            if form.heading.data:
                about_us_content_to_update.heading = form.heading.data
            if form.subheading.data:

                about_us_content_to_update.subheading = form.subheading.data
            if form.description.data:
                about_us_content_to_update.description = form.description.data
            if form.content_url_one.data:
                about_us_content_to_update.content_url_one = form.content_url_one.data
            if form.content_url_two.data:
                about_us_content_to_update.content_url_two = form.content_url_two.data

            # Handle file uploads for images
            for image_field in ['image_one', 'image_two']:
                image_data = getattr(form, image_field).data
                if image_data:
                    # Save the new image
                    filename = secure_filename(image_data.filename)
                    relative_path = os.path.join('uploads', 'about_us', filename).replace("\\", "/")
                    full_path = os.path.join('static', relative_path)
                    image_data.save(full_path)

                    # Delete old image if it exists
                    old_image_path = getattr(about_us_content_to_update, image_field)
                    if old_image_path and os.path.exists(os.path.join('static', old_image_path)):
                        os.remove(os.path.join('static', old_image_path))

                    # Update the new image path in the database
                    setattr(about_us_content_to_update, image_field, relative_path)

            db.session.commit()
            flash('About Us Page Content updated successfully.', 'success')
            return redirect(url_for('dashboard_bp.update_about_us_page'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')

    return render_template(
        'dashboard/about_us/update-about-us-content.html',
        form=form,
        about_us=about_us_content_to_update
    )
