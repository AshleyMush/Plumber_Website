# Route for authentication
from forms.auth import RegisterForm, LoginForm, ForgotPasswordForm, ResetPasswordForm
from flask_login import login_user, current_user, logout_user
from models.user import User, db
from flask import Blueprint, render_template, redirect, url_for, flash, current_app, session
from utils.encryption import hash_and_salt_password, check_password_hash
from utils.email_utils import send_password_reset_email

from . import auth_bp
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from flask import request
import os



@auth_bp.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard_bp.company_profile'))

    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        result = db.session.execute(db.select(User).where(User.email == email))
        user = result.scalar()

        if user and check_password_hash(user.password, password):
            login_user(user, remember=form.remember_me.data)
            flash('Logged in successfully', 'success')
            return redirect(url_for('dashboard_bp.company_profile'))
        else:
            flash('Invalid Email or Password. Please try again.', 'danger')

    return render_template("/auth/login.html", form=form)



#

@auth_bp.route('/logout')
def logout():
    """
    This function logs out the dashboard and redirects them to the BLOG page.
    :return:
    """
    session.clear()
    logout_user()

    return redirect(url_for('website_bp.home'))






@auth_bp.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    user_count = User.query.count()

    if user_count == 0:
        role = 'Admin'
    else:
        flash('Registration is currently closed.', 'info')
        return redirect(url_for('auth_bp.login'))

    if form.validate_on_submit():
        # Generic response, regardless of email existence
        flash('Registration successful. Please log in.', 'success')

        # If email doesn't exist, register the user
        result = db.session.execute(db.select(User).where(User.email == form.email.data))
        user = result.scalar()
        if not user:
            hashed_password = hash_and_salt_password(form.password.data)
            new_user = User(
                email=form.email.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                password=hashed_password,
                role=role
            )
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('auth_bp.login'))

    return render_template("/auth/register.html", form=form)


@auth_bp.route('/forgot-password', methods=["GET", "POST"])
def forgot_password():
    #TODO: REMOVE ME
    current_app.logger.info("Forgot password email triggered.")

    form = ForgotPasswordForm()
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        flash('If an account exists with this email, a reset link has been sent.', 'info')
        if user:
            send_password_reset_email(user.email)
        return redirect(url_for('auth_bp.login'))
    return render_template("/auth/forgot-password.html", form=form)



@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    form = ResetPasswordForm()
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

    try:
        # Decode token to get email
        email = serializer.loads(token, salt=os.environ.get('PASSWORD_RESET_SALT')  , max_age=3600)

    except SignatureExpired:
        flash('The password reset link has expired.', 'danger')
        return redirect(url_for('auth_bp.forgot_password'))
    except BadSignature:
        flash('Invalid password reset link.', 'danger')
        return redirect(url_for('auth_bp.forgot_password'))

    if form.validate_on_submit():
        # Validate and update the password
        user = User.query.filter_by(email=email).first()
        if not user:
            flash('User not found.', 'danger')
            return redirect(url_for('auth_bp.register'))

        # Hash and save the new password
        hashed_password = hash_and_salt_password(form.password.data)
        user.password = hashed_password
        db.session.commit()

        flash('Your password has been successfully updated.', 'success')
        return redirect(url_for('auth_bp.login'))

    return render_template('/auth/reset-password.html', form=form, token=token)