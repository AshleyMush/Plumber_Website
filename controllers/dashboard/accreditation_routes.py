from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required
from models import db,Accreditation
from forms import AccreditationForm
from . import dashboard_bp
from utils.decorators import roles_required
from forms import HomePageContentForm
from werkzeug.utils import secure_filename

import os



UPLOAD_FOLDER = 'static/uploads/accreditations'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@dashboard_bp.route('/accreditations', methods=['GET'])
@roles_required('Admin')
@login_required
def list_accreditations():
    accreditations = Accreditation.query.all()
    return render_template('accreditations.html', accreditations=accreditations)

@dashboard_bp.route('/accreditation/update/<int:id>', methods=['POST'])
@roles_required('Admin')
@login_required
def update_accreditation(id):
    """
    Update an existing accreditation
    """
    accreditation = Accreditation.query.get_or_404(id)
    form = AccreditationForm(obj=accreditation)

    if form.validate_on_submit():
        # Only update non-empty fields
        if form.name.data:
            accreditation.name = form.name.data
        if form.description.data:
            accreditation.description = form.description.data
        if form.image.data:
            # Handle image upload
            filename = secure_filename(form.image.data.filename)
            image_path = os.path.join(UPLOAD_FOLDER, filename)
            form.image.data.save(image_path)
            accreditation.image = image_path

        db.session.commit()
        flash('Accreditation updated successfully.', 'success')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{getattr(form, field).label.text}: {error}", 'danger')

    return redirect(url_for('dashboard_bp.get_accreditations'))


@dashboard_bp.route('/accreditation/delete/<int:id>', methods=['POST'])
@roles_required('Admin')
@login_required
def delete_accreditation(id):
    """
    Delete an accreditation
    """
    accreditation = Accreditation.query.get_or_404(id)
    if accreditation.image and os.path.exists(accreditation.image):
        os.remove(accreditation.image)
    db.session.delete(accreditation)
    db.session.commit()
    flash('Accreditation deleted successfully.', 'info')
    return redirect(url_for('dashboard_bp.get_accreditations'))