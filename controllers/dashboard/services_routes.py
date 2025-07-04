from flask import render_template, redirect, url_for, flash, request, session
from flask_login import current_user, login_required
from utils.decorators import roles_required, nocache
from datetime import date
from werkzeug.utils import secure_filename
from utils.file_upload_helper import save_file
from models import db, Services
from utils.encryption import check_password_hash, generate_password_hash
from . import dashboard_bp
from forms import ServicesForm
import os

# ----------------- Services ----------------- #

@dashboard_bp.route('/add-service', methods=['GET', 'POST'])
@roles_required('Admin')
def add_service():
    """
    Adds a new service with multiple file uploads, ensuring no more than 6 services exist.
    """
    form = ServicesForm()

    # Check the current number of services in the database
    max_services = 6
    total_services = Services.query.count()

    if total_services >= max_services:
        flash(f'You cannot add more than {max_services} services.', 'danger')
        return redirect(url_for('dashboard_bp.get_services'))

    if form.validate_on_submit():
        try:
            # Save all uploaded files
            main_image_path = save_file(form.main_image_path.data, subfolder='services') if form.main_image_path.data else None
            image_one_path = save_file(form.image_one_path.data, subfolder='services') if form.image_one_path.data else None
            image_two_path = save_file(form.image_two_path.data, subfolder='services') if form.image_two_path.data else None

            # Optional content_one_url
            content_one_url = form.content_one_url.data or None

            # Create the new service object
            new_service = Services(
                name=form.name.data,
                main_image_path=main_image_path,
                home_page_card_text=form.home_page_card_text.data,
                header_description=form.header_description.data,
                icon_class=form.icon_class.data,
                feature_heading_one=form.feature_heading_one.data,
                feature_description_one=form.feature_description_one.data,
                image_one_path=image_one_path,
                feature_heading_two=form.feature_heading_two.data,
                feature_description_two=form.feature_description_two.data,
                image_two_path=image_two_path,
                content_one_url=content_one_url
            )

            # Commit the service to the database
            db.session.add(new_service)
            db.session.commit()
            flash('Service added successfully!', 'success')
            return redirect(url_for('dashboard_bp.get_services'))

        except Exception as e:
            db.session.rollback()
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
    This function retrieves all services from the database and calculates progress.
    """
    services = Services.query.all()
    total_services = len(services)
    max_services = 6  # Define the maximum number of services
    progress_percentage = min(int((total_services / max_services) * 100), 100)  # Cap at 100%
    progress_color = get_progress_color(progress_percentage)  # Get the color based on progress

    return render_template(
        '/dashboard/services/services.html',
        services=services,
        progress_percentage=progress_percentage,
        progress_color=progress_color
    )



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
            # Convert '/static/...path...' to 'static/...path...'
            old_full_path = file_path.lstrip('/')
            if os.path.exists(old_full_path):
                os.remove(old_full_path)

    # Delete the service from the database
    db.session.delete(service_to_delete)
    db.session.commit()
    flash('Service deleted successfully', 'info')
    return redirect(url_for('dashboard_bp.get_services'))


@dashboard_bp.route('/update-service/<int:service_id>', methods=['GET', 'POST'])
@roles_required('Admin')
def update_service(service_id):
    """
    Updates an existing service with new data and file uploads using the updated save_file helper.
    """
    service_to_update = Services.query.get_or_404(service_id)
    form = ServicesForm(obj=service_to_update)  # Pre-populate with existing data

    if form.validate_on_submit():
        # Update text fields
        if form.name.data:
            service_to_update.name = form.name.data
        if form.home_page_card_text.data:
            service_to_update.home_page_card_text = form.home_page_card_text.data
        if form.header_description.data:
            service_to_update.header_description = form.header_description.data
        if form.icon_class.data:
            service_to_update.icon_class = form.icon_class.data
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
            service_to_update.main_image_path = save_file(form.main_image_path.data, subfolder='services')
            if old_main_image:
                old_full_path = old_main_image.lstrip('/')
                if os.path.exists(old_full_path):
                    os.remove(old_full_path)

        if form.image_one_path.data and hasattr(form.image_one_path.data, 'filename'):
            old_image_one = service_to_update.image_one_path
            service_to_update.image_one_path = save_file(form.image_one_path.data, subfolder='services')
            if old_image_one:
                old_full_path = old_image_one.lstrip('/')
                if os.path.exists(old_full_path):
                    os.remove(old_full_path)

        if form.image_two_path.data and hasattr(form.image_two_path.data, 'filename'):
            old_image_two = service_to_update.image_two_path
            service_to_update.image_two_path = save_file(form.image_two_path.data, subfolder='services')
            if old_image_two:
                old_full_path = old_image_two.lstrip('/')
                if os.path.exists(old_full_path):
                    os.remove(old_full_path)

        # Commit updates to the database
        db.session.commit()
        flash('Service updated successfully', 'success')
        return redirect(url_for('dashboard_bp.get_services'))

    return render_template('dashboard/services/update-service.html', form=form, service=service_to_update)


def get_progress_color(percentage):
    """
    Determine the color class for the progress bar based on the percentage.
    """
    if percentage >= 75:
        return 'bg-success'  # Green
    elif 50 <= percentage < 75:
        return 'bg-warning'  # Yellow
    else:
        return 'bg-danger'  # Red

