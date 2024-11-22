from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required
from models import db, CompanyDetails, Socials
from forms import CompanyDetailsForm, SocialsForm
from . import dashboard_bp
from utils.decorators import roles_required
import os
from werkzeug.utils import secure_filename



UPLOAD_FOLDER = 'static/uploads/company_logos/'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}


@dashboard_bp.route('/company-profile', methods=['GET'])
@roles_required('Admin')
@login_required
def company_profile():
    # Load existing instances or initialize empty forms if not found
    company_details = CompanyDetails.query.first()
    socials = Socials.query.first()

    # Forms with existing data
    company_form = CompanyDetailsForm(obj=company_details)
    socials_form = SocialsForm(obj=socials)

    return render_template(
        'dashboard/profile/company-profile.html',
        company_form=company_form,
        socials_form=socials_form
    )


@dashboard_bp.route('/company-profile/update-company', methods=['POST'])
@roles_required('Admin')
@login_required
def update_company():
    company_details = CompanyDetails.query.first()
    company_form = CompanyDetailsForm()

    if company_form.validate_on_submit():
        if not company_details:
            company_details = CompanyDetails()
            db.session.add(company_details)

        # Update fields only if they are not blank
        if company_form.name.data:
            company_details.name = company_form.name.data
        if company_form.address.data:
            company_details.address = company_form.address.data
        if company_form.motto.data:
            company_details.motto = company_form.motto.data
        if company_form.about.data:
            company_details.about = company_form.about.data
        if company_form.openingHours.data:
            company_details.openingHours = company_form.openingHours.data
        if company_form.weekendHours.data:
            company_details.weekendHours = company_form.weekendHours.data

        # Handle logo upload
        if company_form.logo.data:
            logo_file = company_form.logo.data
            if logo_file.filename != '':
                filename = secure_filename(logo_file.filename)  # Sanitize the filename
                upload_path = os.path.join(UPLOAD_FOLDER, filename)

                # Delete the old logo file if it exists
                if company_details.logo:
                    old_logo_path = os.path.join(UPLOAD_FOLDER, company_details.logo)
                    if os.path.exists(old_logo_path):
                        os.remove(old_logo_path)

                # Save the new logo file
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure the directory exists
                logo_file.save(upload_path)

                # Update the logo field in the database
                company_details.logo = filename

        db.session.commit()
        flash('Company details updated successfully, including the logo.', 'success')
    else:
        for field, errors in company_form.errors.items():
            for error in errors:
                flash(f"{getattr(company_form, field).label.text}: {error}", 'danger')

    return redirect(url_for('dashboard_bp.company_profile'))

@dashboard_bp.route('/company-profile/update-socials', methods=['POST'])
@roles_required('Admin')
@login_required
def update_socials():
    socials_form = SocialsForm()
    socials = Socials.query.first()

    if socials_form.validate_on_submit():
        if not socials:
            socials = Socials()
            db.session.add(socials)

        # Only update non-empty fields
        if socials_form.instagram.data:
            socials.instagram = socials_form.instagram.data
        if socials_form.whatsapp.data:
            socials.whatsapp = socials_form.whatsapp.data
        if socials_form.youtube.data:
            socials.youtube = socials_form.youtube.data
        if socials_form.facebook.data:
            socials.facebook = socials_form.facebook.data
        if socials_form.threads.data:
            socials.threads = socials_form.threads.data
        if socials_form.x.data:
            socials.x = socials_form.x.data

        db.session.commit()
        flash('Social media links updated successfully.', 'success')
    else:
        for field, errors in socials_form.errors.items():
            for error in errors:
                flash(f"{getattr(socials_form, field).label.text}: {error}", 'danger')

    return redirect(url_for('dashboard_bp.company_profile'))
