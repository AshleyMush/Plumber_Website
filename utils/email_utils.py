# utils/email_utils.py
from flask import render_template, flash,url_for, current_app
from itsdangerous import URLSafeTimedSerializer
import smtplib
from email.mime.text import MIMEText
import os
from datetime import datetime





def send_user_response_email(name, email, subject, service='gmail'):
    """
    Sends a confirmation email to the user.
    """
    ADMIN_EMAIL_ADDRESS = os.environ.get("ADMIN_EMAIL_KEY")
    ADMIN_EMAIL_PW = current_app.config.get('ADMIN_EMAIL_PW')


    from email.mime.text import MIMEText
    import smtplib
    from flask import render_template, flash
    from datetime import datetime

    current_year = datetime.now().year
    email_content = render_template('email/user_aknowledgement_email.html', name=name, current_year=current_year)

    msg = MIMEText(email_content, 'html')
    msg['From'] = ADMIN_EMAIL_ADDRESS
    msg['To'] = email
    msg['Subject'] = f"Confirmation: {subject}"
    msg['Reply-To'] = ADMIN_EMAIL_ADDRESS

    smtp_settings = {
        'gmail': ('smtp.gmail.com', 587),
        'yahoo': ('smtp.mail.yahoo.com', 587),
        'outlook': ('smtp.office365.com', 587),
        'icloud': ('smtp.mail.me.com', 587)  # iCloud SMTP settings
    }

    smtp_server, smtp_port = smtp_settings.get(service, smtp_settings['gmail'])

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as connection:
            connection.starttls()
            connection.login(ADMIN_EMAIL_ADDRESS, ADMIN_EMAIL_PW)
            connection.sendmail(ADMIN_EMAIL_ADDRESS, email, msg.as_string())
    except Exception as e:
        #flash('Error sending confirmation email. Please try again later.', 'danger')
        pass

def send_admin_email(name, phone, subject, email, message, service='gmail'):

    """
    Sends an email to the dashboard with the contact form details.
    """

    ADMIN_EMAIL_ADDRESS = os.environ.get("ADMIN_EMAIL_KEY")
    ADMIN_EMAIL_PW = current_app.config.get('ADMIN_EMAIL_PW')

    current_year = datetime.now().year
    email_content = render_template('email/admin_email.html', name=name, phone=phone, email=email,current_year=current_year, message=message)

    msg = MIMEText(email_content, 'html')
    msg['From'] = email
    msg['To'] = ADMIN_EMAIL_ADDRESS
    msg['Subject'] = f'{name} contacted your website about {subject}'
    msg['Reply-To'] = email

    smtp_settings = {
        'gmail': ('smtp.gmail.com', 587),
        'yahoo': ('smtp.mail.yahoo.com', 587),
        'outlook': ('smtp.office365.com', 587)
    }

    smtp_server, smtp_port = smtp_settings.get(service, smtp_settings['gmail'])

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as connection:
            connection.starttls()
            connection.login(ADMIN_EMAIL_ADDRESS, ADMIN_EMAIL_PW)
            connection.sendmail(from_addr=email, to_addrs=ADMIN_EMAIL_ADDRESS, msg=msg.as_string())
    except Exception as e:
        flash('Error sending email. Please try again later.', 'danger')


def generate_reset_token(email):
    """
    This function generates a password reset token using SECRET_KEY.
    """
    SECRET_KEY = current_app.config.get('SECRET_KEY')
    PASSWORD_RESET_SALT = current_app.config.get('PASSWORD_RESET_SALT')
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    return serializer.dumps(email, salt=PASSWORD_RESET_SALT)



def send_password_reset_email(email, service='gmail'):
    """
    Sends a password reset email to the user.
    """
    # Fetch configuration values inside the function
    ADMIN_EMAIL_ADDRESS = current_app.config.get('ADMIN_EMAIL_ADDRESS')
    ADMIN_EMAIL_PW = current_app.config.get('ADMIN_EMAIL_PW')
    SECRET_KEY = current_app.config.get('SECRET_KEY')
    PASSWORD_RESET_SALT = current_app.config.get('PASSWORD_RESET_SALT')

    # Ensure required configuration exists
    if not all([ADMIN_EMAIL_ADDRESS, ADMIN_EMAIL_PW, SECRET_KEY, PASSWORD_RESET_SALT]):
        current_app.logger.error('Missing email configuration.')
        flash('Email service is not configured properly. Please contact support.', 'danger')
        return

    # Generate token
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    token = serializer.dumps(email, salt=PASSWORD_RESET_SALT)

    # Construct reset URL
    reset_url = url_for('auth_bp.reset_password', token=token, _external=True)

    # Render email content
    email_content = render_template('email/password_reset_email.html', reset_url=reset_url)

    # Set up email message
    msg = MIMEText(email_content, 'html')
    msg['From'] = ADMIN_EMAIL_ADDRESS
    msg['To'] = email
    msg['Subject'] = "Password Reset Request"
    msg['Reply-To'] = ADMIN_EMAIL_ADDRESS

    # SMTP settings
    smtp_settings = {
        'gmail': ('smtp.gmail.com', 587),
        'yahoo': ('smtp.mail.yahoo.com', 587),
        'outlook': ('smtp.office365.com', 587)
    }
    smtp_server, smtp_port = smtp_settings.get(service, smtp_settings['gmail'])

    # Send email
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as connection:
            connection.starttls()
            connection.login(ADMIN_EMAIL_ADDRESS, ADMIN_EMAIL_PW)
            connection.sendmail(ADMIN_EMAIL_ADDRESS, email, msg.as_string())
        flash('Password reset email sent successfully.', 'info')
    except Exception as e:
        flash('Error sending password reset email. Please try again later.', 'danger')
        current_app.logger.error(f'Error sending password reset email: {e}')



def send_approval_message(name, email, subject, service='gmail'):
    """
    Sends a confirmation email to the dashboard.
    """
    ADMIN_EMAIL_ADDRESS = os.environ.get("ADMIN_EMAIL_KEY")
    ADMIN_EMAIL_PW = current_app.config.get('ADMIN_EMAIL_PW')
    current_year = datetime.now().year
    email_content = render_template('email/contributor_approval_email.html',current_year=current_year, name=name)

    msg = MIMEText(email_content, 'html')
    msg['From'] = ADMIN_EMAIL_ADDRESS
    msg['To'] = email
    msg['Subject'] = f"{subject} {name}"
    msg['Reply-To'] = ADMIN_EMAIL_ADDRESS

    smtp_settings = {
        'gmail': ('smtp.gmail.com', 587),
        'yahoo': ('smtp.mail.yahoo.com', 587),
        'outlook': ('smtp.office365.com', 587)
    }

    smtp_server, smtp_port = smtp_settings.get(service, smtp_settings['gmail'])

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as connection:
            connection.starttls()
            connection.login(ADMIN_EMAIL_ADDRESS, ADMIN_EMAIL_PW)
            connection.sendmail(ADMIN_EMAIL_ADDRESS, email, msg.as_string())
    except Exception as e:
        flash('Error sending confirmation email. Please try again later.', 'danger')


def send_demotion_message(name, email, subject, service='gmail'):
    """
    Sends a confirmation email to the dashboard.
    """
    ADMIN_EMAIL_ADDRESS = os.environ.get("ADMIN_EMAIL_KEY")
    ADMIN_EMAIL_PW = current_app.config.get('ADMIN_EMAIL_PW')

    current_year = datetime.now().year

    email_content = render_template('email/letter_of_regret_email.html',current_year=current_year, name=name)

    msg = MIMEText(email_content, 'html')
    msg['From'] = ADMIN_EMAIL_ADDRESS
    msg['To'] = email
    msg['Subject'] = f"{subject}"
    msg['Reply-To'] = ADMIN_EMAIL_ADDRESS

    smtp_settings = {
        'gmail': ('smtp.gmail.com', 587),
        'yahoo': ('smtp.mail.yahoo.com', 587),
        'outlook': ('smtp.office365.com', 587)
    }

    smtp_server, smtp_port = smtp_settings.get(service, smtp_settings['gmail'])

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as connection:
            connection.starttls()
            connection.login(ADMIN_EMAIL_ADDRESS, ADMIN_EMAIL_PW)
            connection.sendmail(ADMIN_EMAIL_ADDRESS, email, msg.as_string())
    except Exception as e:
        flash('Error sending confirmation email. Please try again later.', 'danger')