# utils/email_utils.py
from flask import render_template, flash,url_for, current_app, request
from itsdangerous import URLSafeTimedSerializer
import smtplib
from email.mime.text import MIMEText
import os
from datetime import datetime

ADMIN_EMAIL_ADDRESS = os.environ.get('ADMIN_EMAIL_ADDRESS')
ADMIN_EMAIL_PW = os.environ.get('ADMIN_EMAIL_PW')
SECRET_KEY = os.environ.get('SECRET_APP_KEY')
PASSWORD_RESET_SALT = os.environ.get('PASSWORD_RESET_SALT')



def send_user_response_email(name, email, subject, service='gmail'):
    """
    Sends a confirmation email to the user.
    """
    # ADMIN_EMAIL_ADDRESS = current_app.config.get('ADMIN_EMAIL_ADDRESS')
    #
    # ADMIN_EMAIL_PW = os.environ.get('ADMIN_EMAIL_PW')


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

    # ADMIN_EMAIL_ADDRESS = current_app.config.get('ADMIN_EMAIL_ADDRESS')
    #
    # ADMIN_EMAIL_PW = os.environ.get('ADMIN_EMAIL_PW')

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
    # Todo: Remove this log
    current_app.logger.info("Generating password reset token.")
    print("PRINTF Generating password reset token.")

    serializer = URLSafeTimedSerializer(SECRET_KEY)
    return serializer.dumps(email, salt=PASSWORD_RESET_SALT)


def send_password_reset_email(email, service='gmail'):
    #Todo: Remove this log
    current_app.logger.info("Password reset email sending process started.")

    print(" THIS IS PRINTF Password reset email sending process started.")

    # Log the configuration status
    current_app.logger.info(f"ADMIN_EMAIL_ADDRESS: {ADMIN_EMAIL_ADDRESS}")
    current_app.logger.info(f"SECRET_KEY: {'Set' if SECRET_KEY else 'Not Set'}")
    current_app.logger.info(f"PASSWORD_RESET_SALT: {'Set' if PASSWORD_RESET_SALT else 'Not Set'}")

    # Ensure required configuration exists
    if not all([ADMIN_EMAIL_ADDRESS, ADMIN_EMAIL_PW, SECRET_KEY, PASSWORD_RESET_SALT]):
        # Todo: Remove this log

        current_app.logger.error('Missing email configuration.')
        print('PRINTF Missing email configuration.')



        flash('Email service is not configured properly. Please contact support.', 'danger')
        return

    # Generate token
    try:
        serializer = URLSafeTimedSerializer(SECRET_KEY)
        token = serializer.dumps(email, salt=PASSWORD_RESET_SALT)
        current_app.logger.info("Token generated successfully.")
    except Exception as e:
        current_app.logger.error(f"Error generating token: {e}")
        print(f" PRINT Error generating token: {e}")

        flash('Error generating reset token. Please try again later.', 'danger')
        return

    # Dynamically build reset URL from the incoming request
    base_url = request.url_root  # e.g. http://127.0.0.1:5002/ or https://<yourapp>.onrender.com/

    # Optionally force HTTPS in production
    if base_url.startswith("http://"):
        base_url = base_url.replace("http://", "https://")

    reset_url = f"{base_url.rstrip('/')}{url_for('auth_bp.reset_password', token=token)}"

    #Todo: Remove this log
    current_app.logger.info(f"Reset URL generated: {reset_url}")
    print(f"PRINTF Reset URL generated: {reset_url}")

    # Render email content
    try:
        email_content = render_template('email/password_reset_email.html', reset_url=reset_url)
        #Todo: Remove this log
        current_app.logger.info("Email content rendered successfully.")
        print("PRINTF Email content rendered successfully.")


    except Exception as e:
        # Todo: Remove this log
        current_app.logger.error(f"Error rendering email content: {e}")
        print(f"PRINTF Error rendering email content: {e}")


        flash('Error rendering email content. Please try again later.', 'danger')
        return

    # Set up email message
    msg = MIMEText(email_content, 'html')
    msg['From'] = ADMIN_EMAIL_ADDRESS
    msg['To'] = email
    msg['Subject'] = "Password Reset Request"
    msg['Reply-To'] = ADMIN_EMAIL_ADDRESS

    # SMTP settings for various providers
    smtp_settings = {
        'gmail': ('smtp.gmail.com', 587),
        'yahoo': ('smtp.mail.yahoo.com', 587),
        'outlook': ('smtp.office365.com', 587),
        'icloud': ('smtp.mail.me.com', 587),
        'hotmail': ('smtp-mail.outlook.com', 587),
    }

    # Fallback to Gmail if the chosen service isn't in the dictionary
    smtp_server, smtp_port = smtp_settings.get(service, smtp_settings['gmail'])

    # Send email
    try:
        #Todo: Remove this log
        current_app.logger.info(f"Connecting to SMTP server: {smtp_server}:{smtp_port}")
        print(f"PRINTF Connecting to SMTP server: {smtp_server}:{smtp_port}")

        with smtplib.SMTP(smtp_server, smtp_port) as connection:
            connection.starttls()
            current_app.logger.info("SMTP connection secured with STARTTLS.")
            connection.login(ADMIN_EMAIL_ADDRESS, ADMIN_EMAIL_PW)

            #Todo: Remove this log
            current_app.logger.info("Logged in to SMTP server successfully.")
            print("PRINTF Logged in to SMTP server successfully.")




            connection.sendmail(ADMIN_EMAIL_ADDRESS, email, msg.as_string())

            #Todo: Remove this log
            current_app.logger.info(f"Email sent successfully to {email}.")
            print(f"PRINTF Email sent successfully to {email}.")

        flash('Password reset email sent successfully.', 'info')
    except smtplib.SMTPException as e:
        #Todo: Remove this log
        current_app.logger.error(f"SMTP error: {e}")
        print(f"PRINTF SMTP error: {e}")

        flash('Error sending password reset email. Please try again later.', 'danger')
    except Exception as e:
        #Todo: Remove this log
        current_app.logger.error(f"Unexpected error sending email: {e}")
        print(f"PRINTF Unexpected error sending email: {e}")

        flash('Error sending password reset email. Please try again later.', 'danger')




def send_approval_message(name, email, subject, service='gmail'):
    """
    Sends a confirmation email to the dashboard.
    """
    # ADMIN_EMAIL_ADDRESS = os.environ.get('ADMIN_EMAIL_ADDRESS')
    #
    # ADMIN_EMAIL_PW = os.environ.get('ADMIN_EMAIL_PW')
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
    # ADMIN_EMAIL_ADDRESS = current_app.config.get('ADMIN_EMAIL_ADDRESS')
    #
    # ADMIN_EMAIL_PW = os.environ.get('ADMIN_EMAIL_PW')

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