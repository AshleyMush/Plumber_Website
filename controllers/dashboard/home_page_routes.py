from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required
from models import db, Home
from forms import HomePageContentForm
from . import dashboard_bp
from utils.decorators import roles_required
from utils.file_upload_helper import save_file
import os

# Configure Upload Folder
UPLOAD_FOLDER = '/static/uploads/home'

@dashboard_bp.app_context_processor
def inject_home_content_status():
    home_exists = Home.query.count() > 0
    return {'home_exists': home_exists}

@dashboard_bp.route('/add-home-content', methods=['GET', 'POST'])
@roles_required('Admin')
@login_required
def add_home_content():
    """
    Add home page content to the database with image uploading capabilities.
    """
    form = HomePageContentForm()
    if form.validate_on_submit():
        try:
            # Handle file uploads for multiple images
            uploaded_images = {}
            for image_field in ['image_one', 'image_two', 'image_three', 'image_four']:
                image_data = getattr(form, image_field).data
                if image_data:
                    uploaded_images[image_field] = save_file(image_data, base_folder=UPLOAD_FOLDER)

            # Add new content to the database
            new_home_content = Home(
                heading=form.heading.data,
                subheading=form.subheading.data,
                description=form.description.data,
                image_one=uploaded_images.get('image_one'),
                image_two=uploaded_images.get('image_two'),
                image_three=uploaded_images.get('image_three'),
                image_four=uploaded_images.get('image_four'),
                content_url_one=form.content_url_one.data,
                content_url_two=form.content_url_two.data,
                content_url_three=form.content_url_three.data,
            )
            db.session.add(new_home_content)
            db.session.commit()
            flash('Home Page Content added successfully', 'success')
            return redirect(url_for('dashboard_bp.update_home_page'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error occurred: {str(e)}', 'danger')
    else:
        if form.errors:
            for field_name, error_list in form.errors.items():
                for error in error_list:
                    flash(f"Error in '{field_name}': {error}", 'danger')

    return render_template('dashboard/home/add-home-content.html', form=form)

@dashboard_bp.route('/update-home-page', methods=['GET', 'POST'])
@roles_required('Admin')
@login_required
def update_home_page():
    """
    Update home page content with image uploading capabilities.
    """
    home_content_to_update = Home.query.first()
    if not home_content_to_update:
        flash("No home content found to update. Please add content first.", 'warning')
        return redirect(url_for('dashboard_bp.add_home_content'))

    form = HomePageContentForm()

    # Pre-fill form with existing data on GET requests
    if request.method == 'GET':
        form.heading.data = home_content_to_update.heading
        form.subheading.data = home_content_to_update.subheading
        form.description.data = home_content_to_update.description
        form.image_one.data = None
        form.image_two.data = None
        form.image_three.data = None
        form.image_four.data = None

    if form.validate_on_submit():
        try:
            # Update text fields
            home_content_to_update.heading = form.heading.data
            home_content_to_update.subheading = form.subheading.data
            home_content_to_update.description = form.description.data

            # Handle file uploads for multiple images
            for image_field in ['image_one', 'image_two', 'image_three', 'image_four']:
                image_data = getattr(form, image_field).data
                if image_data:
                    # Save the new image
                    new_image_path = save_file(image_data, base_folder=UPLOAD_FOLDER)

                    # Delete old image if it exists
                    old_image_path = getattr(home_content_to_update, image_field)
                    if old_image_path:
                        full_old_path = os.path.join('static', old_image_path)
                        if os.path.exists(full_old_path):
                            os.remove(full_old_path)

                    # Update the new image path in the database
                    setattr(home_content_to_update, image_field, new_image_path)

            db.session.commit()
            flash('Home Page Content updated successfully.', 'success')
            return redirect(url_for('dashboard_bp.update_home_page'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')

    return render_template(
        'dashboard/home/update-home-content.html',
        form=form,
        home=home_content_to_update
    )
