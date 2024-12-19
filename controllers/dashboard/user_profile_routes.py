from flask import render_template, redirect, url_for, flash, request, session
from flask_login import current_user, login_required
from utils.decorators import roles_required
from utils.decorators import  nocache
from datetime import date
from utils.email_utils import send_approval_message, send_demotion_message
from . import dashboard_bp
from models import db, User, Home
from utils.encryption import check_password_hash, generate_password_hash
from forms import UpdateEmailForm, UpdatePhoneForm, ChangePasswordForm







@dashboard_bp.route("/user-profile", methods=['POST', 'GET'])
@roles_required('Admin')
@nocache
def user_profile():
    email_form = UpdateEmailForm()
    phone_form = UpdatePhoneForm()
    password_form = ChangePasswordForm()


    email_form.email.data = current_user.email
    phone_form.phone_number.data = current_user.phone_number


    return render_template('dashboard/profile/user-profile.html', email_form=email_form, phone_form=phone_form,
                           password_form=password_form)









@dashboard_bp.route('/update-user-phone-number', methods=['POST'])
@roles_required('Admin')
def update_phone_user_number():
    form = UpdatePhoneForm()
    if form.validate_on_submit():
        phone_number = form.phone_number.data
        current_user.phone_number = phone_number
        db.session.commit()
        flash('Phone number updated successfully, refresh your browser.', 'success')
    else:
        # Handle form validation errors
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{getattr(form, field).label.text}: {error}", 'danger')
    return redirect(url_for('dashboard_bp.profile'))



@dashboard_bp.route('/update-user-email', methods=['POST'])
@roles_required('Admin')
def update_user_email():
    """
    This function updates the All dashboard's email address.
    :return:
    """
    form = UpdateEmailForm()
    if form.validate_on_submit():
        new_email = form.email.data
        current_user.email = new_email
        db.session.commit()
        flash('Email updated successfully, refresh your browser.', 'success')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{getattr(form, field).label.text}: {error}", 'danger')

    return redirect(url_for('dashboard_bp.profile'))



@dashboard_bp.route('/change-user-password', methods=['POST'])
@roles_required('Admin')
def change_user_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        current_password = form.current_password.data
        new_password = form.new_password.data

        if not check_password_hash(current_user.password, current_password):
            flash('Current password is incorrect.', 'danger')
            return redirect(url_for('dashboard_bp.profile'))

        # Update the dashboard's password
        current_user.password = generate_password_hash(new_password)
        db.session.commit()
        flash('Your password has been updated.', 'success')
    else:
        # Handle form validation errors
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{getattr(form, field).label.text}: {error}", 'danger')
    return redirect(url_for('dashboard_bp.profile'))

