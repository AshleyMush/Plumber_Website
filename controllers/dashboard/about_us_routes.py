from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required
from utils.decorators import roles_required
from utils.file_upload_helper import save_file
from models import db, AboutUsPageContent
from forms import AboutUsForm
from . import dashboard_bp
import os

@dashboard_bp.app_context_processor
def inject_home_content_status():
    about_exists = AboutUsPageContent.query.count() > 0
    return {'about_exists': about_exists}


@dashboard_bp.route('/add-about-us-content', methods=['GET', 'POST'])
@roles_required('Admin')
def add_about_us_content():
    """
    Adds About Us page content with image uploads.
    """
    # Check if About Us content already exists
    if AboutUsPageContent.query.first():
        flash('The About Us page has already been set up, you can only modify it.', 'info')

        return redirect(url_for('dashboard_bp.update_about_us_page'))


    form = AboutUsForm()
    if form.validate_on_submit():
        try:
            # Handle file uploads
            main_image_path = save_file(form.main_image_path.data, subfolder='about_us') if form.main_image_path.data else None
            image_one_path = save_file(form.image_one_path.data, subfolder='about_us') if form.image_one_path.data else None
            image_two_path = save_file(form.image_two_path.data, subfolder='about_us') if form.image_two_path.data else None

            # Create new content
            new_content = AboutUsPageContent(
                heading=form.heading.data,
                subheading=form.subheading.data,
                main_image_path=main_image_path,
                image_one_path=image_one_path,
                image_two_path=image_two_path,
                content_one_url=form.content_one_url.data,
                content_two_url=form.content_two_url.data,
                content_three_url=form.content_three_url.data,
                feature_one_heading=form.feature_one_heading.data,
                feature_one_description=form.feature_one_description.data,
                feature_two_heading=form.feature_two_heading.data,
                feature_two_description=form.feature_two_description.data
            )
            db.session.add(new_content)
            db.session.commit()
            flash('About Us content added successfully!', 'success')
            return redirect(url_for('dashboard_bp.update_about_us_page'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')

    return render_template('dashboard/about_us/add-about-us-content.html', form=form)



@dashboard_bp.route('/update-about-us-page', methods=['GET', 'POST'])
@roles_required('Admin')
def update_about_us_page():
    """
    Updates About Us page content and manages file uploads.
    """
    content = AboutUsPageContent.query.first()
    if not content:
        flash('No content found. Please add content first.', 'warning')
        return redirect(url_for('dashboard_bp.add_about_us_content'))

    form = AboutUsForm(obj=content)

    # Clear file fields on GET request
    if request.method == 'GET':
        form.main_image_path.data = None
        form.image_one_path.data = None
        form.image_two_path.data = None

    if form.validate_on_submit():
        try:
            # Update fields
            content.heading = form.heading.data
            content.subheading = form.subheading.data
            content.content_one_url = form.content_one_url.data
            content.content_two_url = form.content_two_url.data
            content.content_three_url = form.content_three_url.data
            content.feature_one_heading = form.feature_one_heading.data
            content.feature_one_description = form.feature_one_description.data
            content.feature_two_heading = form.feature_two_heading.data
            content.feature_two_description = form.feature_two_description.data

            # Manage file uploads
            if form.main_image_path.data:
                old_path = content.main_image_path
                content.main_image_path = save_file(form.main_image_path.data, subfolder='about_us')
                if old_path:
                    os.remove(old_path.lstrip('/'))  # Remove old file

            if form.image_one_path.data:
                old_path = content.image_one_path
                content.image_one_path = save_file(form.image_one_path.data, subfolder='about_us')
                if old_path:
                    os.remove(old_path.lstrip('/'))

            if form.image_two_path.data:
                old_path = content.image_two_path
                content.image_two_path = save_file(form.image_two_path.data, subfolder='about_us')
                if old_path:
                    os.remove(old_path.lstrip('/'))

            db.session.commit()
            flash('About Us content updated successfully!', 'success')
            return redirect(url_for('dashboard_bp.update_about_us_page'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')

    return render_template('dashboard/about_us/update-about-us-content.html', form=form, about_us=content)
