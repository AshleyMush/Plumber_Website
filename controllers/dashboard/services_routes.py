from flask import render_template, redirect, url_for, flash, request, session
from flask_login import current_user, login_required
from utils.decorators import roles_required
from utils.decorators import  nocache
from datetime import date

from models import db, Services
from utils.encryption import check_password_hash, generate_password_hash
from . import dashboard_bp



from forms import ServicesForm




# ----------------- Services ----------------- #

@dashboard_bp.route('/add-service', methods=['GET', 'POST'])
@roles_required('Admin')
def add_service():
    """
    This function adds a service to the database
    """
    form = ServicesForm()  # Assumes you have a ServiceForm for handling input
    if form.validate_on_submit():
        new_service = Services(
            name=form.name.data,
            homeImage=form.homeImage.data,
            homeDescription=form.homeDescription.data,
            description=form.description.data
        )
        db.session.add(new_service)
        db.session.commit()
        flash('Service added successfully', 'success')
        return redirect(url_for('dashboard_bp.get_services'))
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
    This function deletes a service from the database
    """
    service_to_delete = Services.query.get_or_404(service_id)
    db.session.delete(service_to_delete)
    db.session.commit()
    flash('Service deleted successfully', 'info')
    return redirect(url_for('dashboard_bp.get_services'))


@dashboard_bp.route('/update-service/<int:service_id>', methods=['GET', 'POST'])
@roles_required('Admin')
def update_service(service_id):
    """
    This function updates a service in the database
    """
    service_to_update = Services.query.get_or_404(service_id)
    form = ServicesForm(obj=service_to_update)  # Pre-populate with existing data

    if form.validate_on_submit():
        # Update only the fields that are not left blank
        if form.name.data:
            service_to_update.name = form.name.data
        if form.homeImage.data:
            service_to_update.homeImage = form.homeImage.data
        if form.homeDescription.data:
            service_to_update.homeDescription = form.homeDescription.data
        if form.description.data:
            service_to_update.description = form.description.data

        db.session.commit()
        flash('Service updated successfully', 'success')
        return redirect(url_for('dashboard_bp.get_services'))

    return render_template('dashboard/services/update-service.html', form=form, service=service_to_update)

