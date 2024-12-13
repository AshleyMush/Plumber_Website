from flask import render_template, redirect, url_for, flash, request, session
from flask_login import current_user, login_required
from utils.decorators import roles_required
from utils.decorators import  nocache
from datetime import date
from werkzeug.utils import secure_filename
from utils.file_upload_helper import save_file
from models import db, Services
from utils.encryption import check_password_hash, generate_password_hash
from . import dashboard_bp
from forms import ServicesForm
import os

# Configure Upload Folder
UPLOAD_FOLDER = 'uploads/services'





# ----------------- Services ----------------- #

@dashboard_bp.route('/add-service', methods=['GET', 'POST'])
@roles_required('Admin')
def add_service():
    """
    Adds a new service with multiple file uploads.
    """
    form = ServicesForm()
    if form.validate_on_submit():
        try:
            # Save all uploaded files
            main_image_path = save_file(form.main_image_path.data, base_folder=UPLOAD_FOLDER)
            image_one_path = save_file(form.image_one_path.data, base_folder=UPLOAD_FOLDER)
            image_two_path = save_file(form.image_two_path.data, base_folder=UPLOAD_FOLDER)

            # Optional content_one_url
            content_one_url = form.content_one_url.data or None

            # Create the new service object
            new_service = Services(
                name=form.name.data,
                main_image_path=main_image_path,
                home_page_card_text=form.home_page_card_text.data,
                header_description=form.header_description.data,
                feature_heading_one=form.feature_heading_one.data,
                feature_description_one=form.feature_description_one.data,
                image_one_path=image_one_path,
                feature_heading_two=form.feature_heading_two.data,
                feature_description_two=form.feature_description_two.data,
                image_two_path=image_two_path,
                content_one_url=content_one_url  # Optional field
            )

            # Commit the service to the database
            db.session.add(new_service)
            db.session.commit()
            flash('Service added successfully!', 'success')
            return redirect(url_for('dashboard_bp.get_services'))

        except Exception as e:
            db.session.rollback()  # Ensure no partial changes
            flash(f'Error occurred: {str(e)}', 'danger')

    if form.errors:  # Display validation errors
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in the {field} field - {error}", 'danger')

    return render_template('dashboard/services/add-service.html', form=form)


@dashboard_bp.route('/services', methods=['GET'])
@roles_required('Admin')
def get_services():
    """
    This function retrieves all services from the database
    """
    services = Services.query.all()
    return render_template('/dashboard/services/services.html', services=services)


@dashboard_bp.route('/delete-service/<int:service_id>', methods=['GET', 'DELETE'])
@roles_required('Admin')
def delete_service(service_id):
    """
    Deletes a service and its associated uploaded files.
    """
    service_to_delete = Services.query.get_or_404(service_id)

    # Remove all associated uploaded files
    file_paths = [
        service_to_delete.main_image_path,
        service_to_delete.image_one_path,
        service_to_delete.image_two_path,
    ]

    for file_path in file_paths:
        if file_path:
            full_path = os.path.join('static', file_path)
            if os.path.exists(full_path):
                os.remove(full_path)

    # Delete the service from the database
    db.session.delete(service_to_delete)
    db.session.commit()
    flash('Service deleted successfully', 'info')
    return redirect(url_for('dashboard_bp.get_services'))



@dashboard_bp.route('/update-service/<int:service_id>', methods=['GET', 'POST'])
@roles_required('Admin')
def update_service(service_id):
    """
    Updates an existing service with new data and file uploads.
    """
    service_to_update = Services.query.get_or_404(service_id)
    form = ServicesForm(obj=service_to_update)  # Pre-populate with existing data

    if form.validate_on_submit():
        # Update fields if data is provided
        if form.name.data:
            service_to_update.name = form.name.data
        if form.home_page_card_text.data:
            service_to_update.home_page_card_text = form.home_page_card_text.data
        if form.header_description.data:
            service_to_update.header_description = form.header_description.data
        if form.feature_heading_one.data:
            service_to_update.feature_heading_one = form.feature_heading_one.data
        if form.feature_description_one.data:
            service_to_update.feature_description_one = form.feature_description_one.data
        if form.feature_heading_two.data:
            service_to_update.feature_heading_two = form.feature_heading_two.data
        if form.feature_description_two.data:
            service_to_update.feature_description_two = form.feature_description_two.data
        if form.content_one_url.data:
            service_to_update.content_one_url = form.content_one_url.data

        # Handle file uploads and remove old files if a new file is uploaded
        if form.main_image_path.data and hasattr(form.main_image_path.data, 'filename'):
            old_main_image = service_to_update.main_image_path
            service_to_update.main_image_path = save_file(form.main_image_path.data, base_folder=UPLOAD_FOLDER)
            if old_main_image:
                full_path = os.path.join('static', old_main_image)
                if os.path.exists(full_path):
                    os.remove(full_path)

        if form.image_one_path.data and hasattr(form.image_one_path.data, 'filename'):
            old_image_one = service_to_update.image_one_path
            service_to_update.image_one_path = save_file(form.image_one_path.data, base_folder=UPLOAD_FOLDER)
            if old_image_one:
                full_path = os.path.join('static', old_image_one)
                if os.path.exists(full_path):
                    os.remove(full_path)

        if form.image_two_path.data and hasattr(form.image_two_path.data, 'filename'):
            old_image_two = service_to_update.image_two_path
            service_to_update.image_two_path = save_file(form.image_two_path.data, base_folder=UPLOAD_FOLDER)
            if old_image_two:
                full_path = os.path.join('static', old_image_two)
                if os.path.exists(full_path):
                    os.remove(full_path)

        # Commit updates to the database
        db.session.commit()
        flash('Service updated successfully', 'success')
        return redirect(url_for('dashboard_bp.get_services'))

    return render_template('dashboard/services/update-service.html', form=form, service=service_to_update)


