from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required
from models import db, Accreditation
from forms import AccreditationForm
from . import dashboard_bp
from utils.decorators import roles_required
from utils.file_upload_helper import save_file
import os


@dashboard_bp.route('/accreditations', methods=['GET'])
@roles_required('Admin')
@login_required
def get_accreditations():
    """
    List all accreditations
    """
    accreditations = Accreditation.query.all()
    return render_template(
        'dashboard/accreditations/accreditations.html',
        accreditations=accreditations
    )


@dashboard_bp.route('/accreditation/add', methods=['GET', 'POST'])
@roles_required('Admin')
@login_required
def add_accreditation():
    """
    Add a new accreditation using the save_file helper.
    """
    form = AccreditationForm()
    if form.validate_on_submit():
        # Handle file upload with the helper function
        image_path = save_file(form.image.data, subfolder='accreditations') if form.image.data else None

        # Add to the database
        new_accreditation = Accreditation(
            name=form.name.data,
            image=image_path,
            description=form.description.data
        )
        db.session.add(new_accreditation)
        db.session.commit()
        flash('Accreditation added successfully.', 'success')
        return redirect(url_for('dashboard_bp.get_accreditations'))

    return render_template(
        'dashboard/accreditations/add-accreditation.html',
        form=form
    )


@dashboard_bp.route('/accreditation/update/<int:accreditation_id>', methods=['GET', 'POST'])
@roles_required('Admin')
@login_required
def update_accreditation(accreditation_id):
    """
    Update an existing accreditation using the save_file helper.
    """
    accreditation = Accreditation.query.get_or_404(accreditation_id)
    form = AccreditationForm(obj=accreditation)

    if form.validate_on_submit():
        # Update text fields if provided
        accreditation.name = form.name.data or accreditation.name
        accreditation.description = form.description.data or accreditation.description

        if form.image.data:
            # Save the new image
            new_image_path = save_file(form.image.data, subfolder='accreditations')
            # Delete the old image if it exists
            if accreditation.image:
                old_full_path = accreditation.image.lstrip('/')  # Convert '/static/...'
                if os.path.exists(old_full_path):
                    os.remove(old_full_path)

            accreditation.image = new_image_path

        db.session.commit()
        flash('Accreditation updated successfully.', 'success')
        return redirect(url_for('dashboard_bp.get_accreditations'))

    return render_template(
        'dashboard/accreditations/update-accreditation.html',
        form=form,
        accreditation=accreditation
    )


@dashboard_bp.route('/accreditation/delete/<int:accreditation_id>', methods=['DELETE', 'GET'])
@roles_required('Admin')
@login_required
def delete_accreditation(accreditation_id):
    """
    Delete an accreditation and its associated image using the updated logic.
    """
    accreditation = Accreditation.query.get_or_404(accreditation_id)

    # Delete the associated image file if it exists
    if accreditation.image:
        old_full_path = accreditation.image.lstrip('/')  # Convert '/static/...'
        if os.path.exists(old_full_path):
            os.remove(old_full_path)

    db.session.delete(accreditation)
    db.session.commit()
    flash('Accreditation deleted successfully.', 'info')
    return redirect(url_for('dashboard_bp.get_accreditations'))
