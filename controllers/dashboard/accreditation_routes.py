from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required
from models import db, Accreditation
from forms import AccreditationForm
from . import dashboard_bp
from utils.decorators import roles_required
from werkzeug.utils import secure_filename
import os

# Configure Upload Folder
UPLOAD_FOLDER = 'static/uploads/accreditations'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

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
    Add a new accreditation
    """
    form = AccreditationForm()
    if form.validate_on_submit():
        # Handle file upload
        image_path = None
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            # Ensure the path uses forward slashes for URLs
            relative_path = os.path.join('uploads', 'accreditations', filename).replace("\\", "/")
            full_path = os.path.join('static', relative_path)  # Full path for saving
            form.image.data.save(full_path)

            # Save the relative path to the database
            image_path = relative_path

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

@dashboard_bp.route('/accreditation/update/<int:id>', methods=['GET', 'POST'])
@roles_required('Admin')
@login_required
def update_accreditation(id):
    """
    Update an existing accreditation
    """
    accreditation = Accreditation.query.get_or_404(id)
    form = AccreditationForm(obj=accreditation)  # Pre-fill the form with existing data

    if form.validate_on_submit():
        # Update fields only if data is provided
        accreditation.name = form.name.data or accreditation.name
        accreditation.description = form.description.data or accreditation.description
        if form.image.data:
            # Save new image
            filename = secure_filename(form.image.data.filename)
            relative_path = os.path.join('uploads', 'accreditations', filename).replace("\\", "/")
            full_path = os.path.join('static', relative_path)
            form.image.data.save(full_path)

            # Delete the old image if it exists
            if accreditation.image and os.path.exists(os.path.join('static', accreditation.image)):
                os.remove(os.path.join('static', accreditation.image))

            accreditation.image = relative_path  # Update the image path in the database

        db.session.commit()
        flash('Accreditation updated successfully.', 'success')
        return redirect(url_for('dashboard_bp.get_accreditations'))

    return render_template(
        'dashboard/accreditations/update-accreditation.html',
        form=form,
        accreditation=accreditation
    )

@dashboard_bp.route('/accreditation/delete/<int:id>', methods=['DETETE','GET'])
@roles_required('Admin')
@login_required
def delete_accreditation(id):
    """
    Delete an accreditation
    """
    accreditation = Accreditation.query.get_or_404(id)
    # Delete the associated image file if it exists
    if accreditation.image and os.path.exists(os.path.join('static', accreditation.image)):
        os.remove(os.path.join('static', accreditation.image))
    db.session.delete(accreditation)
    db.session.commit()
    flash('Accreditation deleted successfully.', 'info')
    return redirect(url_for('dashboard_bp.get_accreditations'))
