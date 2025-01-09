from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, CompanyDetails, Socials
from forms import CompanyDetailsForm, SocialsForm, UpdateEmailForm, UpdatePhoneForm, ChangePasswordForm
from . import dashboard_bp
from utils.decorators import roles_required
from utils.encryption import check_password_hash, generate_password_hash
from utils.file_upload_helper import save_file
import os


@dashboard_bp.route('/company-profile/update-company', methods=['POST'])
@roles_required('Admin')
@login_required
def update_company_details():
    company_details = CompanyDetails.query.first()
    company_form = CompanyDetailsForm()

    if company_form.validate_on_submit():
        # If there's no existing company_details record, create one.
        if not company_details:
            company_details = CompanyDetails()
            db.session.add(company_details)

        # Update text fields if provided
        if company_form.name.data:
            company_details.name = company_form.name.data
        if company_form.address.data:
            company_details.address = company_form.address.data
        if company_form.map_snippet.data:
            company_details.map_snippet = company_form.map_snippet.data
        if company_form.motto.data:
            company_details.motto = company_form.motto.data
        if company_form.about.data:
            company_details.about = company_form.about.data
        if company_form.openingHours.data:
            company_details.openingHours = company_form.openingHours.data
        if company_form.weekendHours.data:
            company_details.weekendHours = company_form.weekendHours.data

        # Handle logo upload using save_file helper
        if company_form.logo.data:
            # Save the new logo and get its web-accessible path
            new_logo_path = save_file(company_form.logo.data, subfolder='logos')

            # If there's an old logo, remove it
            if company_details.logo:
                old_full_path = company_details.logo.lstrip('/')
                if os.path.exists(old_full_path):
                    os.remove(old_full_path)

            # Update the logo field to the new path
            company_details.logo = new_logo_path

        # Update the show_location field
        company_details.show_location = company_form.show_location.data

        db.session.commit()
        flash('Company details updated successfully.', 'success')
    else:
        # Display form validation errors
        for field, errors in company_form.errors.items():
            for error in errors:
                flash(f"{getattr(company_form, field).label.text}: {error}", 'danger')

    return redirect(url_for('dashboard_bp.company_profile'))






@dashboard_bp.route('/company-profile', methods=['GET'])
@roles_required('Admin')
@login_required
def company_profile():
    # Load existing instances or initialize empty forms if not found
    company_details = CompanyDetails.query.first()
    socials = Socials.query.first()
    email_form = UpdateEmailForm()
    phone_form = UpdatePhoneForm()
    password_form = ChangePasswordForm()

    # Forms with existing data
    company_form = CompanyDetailsForm(obj=company_details)
    socials_form = SocialsForm(obj=socials)

    return render_template(
        'dashboard/profile/company-profile.html',
        company_form=company_form,
        socials_form=socials_form,
        company_details = company_details,
        password_form=password_form,
        email_form=email_form,
        phone_form=phone_form

    )




@dashboard_bp.route('/update-email', methods=['POST'])
@roles_required('Admin')
def update_email():
    """
    This function updates the All dashboard's email address.
    :return:
    """
    company_details = CompanyDetails.query.first()
    if company_details is None:
        company_details = CompanyDetails()
        db.session.add(company_details)

    form = UpdateEmailForm()
    if form.validate_on_submit() and form.email.data:
        new_email = form.email.data
        company_details.email = new_email
        db.session.commit()
        flash('Email updated successfully, refresh your browser.', 'success')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{getattr(form, field).label.text}: {error}", 'danger')

    return redirect(url_for('dashboard_bp.company_profile'))


@dashboard_bp.route('/update-phone-number', methods=['POST'])
@roles_required('Admin')
def update_phone_number():
    company_details = CompanyDetails.query.first()

    if company_details is None:
        company_details = CompanyDetails()
        db.session.add(company_details)

    form = UpdatePhoneForm()
    if form.validate_on_submit() and form.phone_number.data:
        phone_number = form.phone_number.data
        company_details.phone = phone_number
        db.session.commit()
        flash('Phone number updated successfully, refresh your browser.', 'success')
    else:
        # Handle form validation errors
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{getattr(form, field).label.text}: {error}", 'danger')
    return redirect(url_for('dashboard_bp.company_profile'))


@dashboard_bp.route('/change-password', methods=['POST'])
@roles_required('Admin')
def change_password():

    form = ChangePasswordForm()
    if form.validate_on_submit():
        current_password = form.current_password.data
        new_password = form.new_password.data

        if not check_password_hash(current_user.password, current_password):
            flash('Current password is incorrect.', 'danger')
            return redirect(url_for('dashboard_bp.company_profile'))

        # Update the dashboard's password
        current_user.password = generate_password_hash(new_password)
        db.session.commit()
        flash('Your password has been updated.', 'success')
    else:
        # Handle form validation errors
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{getattr(form, field).label.text}: {error}", 'danger')
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
