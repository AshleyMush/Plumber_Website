from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required
from models import db, AboutUsPageContent
from forms import AboutUsForm
from . import dashboard_bp
from utils.decorators import roles_required
from utils.file_upload_helper import save_file
import os

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
            # Handle file uploads using the helper function
            image_one_path = save_file(form.image_one.data, subfolder='about_us') if form.image_one.data else None
            image_two_path = save_file(form.image_two.data, subfolder='about_us') if form.image_two.data else None

            # Add new content to the database
            new_about_us_content = AboutUsPageContent(
                heading=form.heading.data,
                subheading=form.subheading.data,
                description=form.description.data,
                image_one=image_one_path,
                image_two=image_two_path,
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

    form = AboutUsForm(obj=about_us_content_to_update)

    # Clear file fields on GET request
    if request.method == 'GET':
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
            # If a new image is provided, save it and remove the old one if it exists
            if form.image_one.data:
                new_image_one_path = save_file(form.image_one.data, subfolder='about_us')
                if about_us_content_to_update.image_one:
                    old_full_path = about_us_content_to_update.image_one.lstrip('/')
                    if os.path.exists(old_full_path):
                        os.remove(old_full_path)
                about_us_content_to_update.image_one = new_image_one_path

            if form.image_two.data:
                new_image_two_path = save_file(form.image_two.data, subfolder='about_us')
                if about_us_content_to_update.image_two:
                    old_full_path = about_us_content_to_update.image_two.lstrip('/')
                    if os.path.exists(old_full_path):
                        os.remove(old_full_path)
                about_us_content_to_update.image_two = new_image_two_path

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
