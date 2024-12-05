from . import website_bp
from forms import ContactUSForm
from flask import render_template, flash, url_for, redirect
from utils.email_utils import send_admin_email, send_user_response_email
from models import db, User, Home
import bleach # For sanitizing HTML
from datetime import datetime


CURRENT_YEAR = datetime.now().year



@website_bp.route('/contact-us', methods=['GET', 'POST'])
def contact():
    form = ContactUSForm()
    user = User.query.first()

    if form.validate_on_submit():
        name = bleach.clean(form.name.data)
        email = bleach.clean(form.email.data)
        phone = bleach.clean(form.phone.data)
        subject = bleach.clean(form.subject.data)
        message = bleach.clean(form.message.data)

        flash('Message sent successfully', 'success')
        # Send the email to the admin
        send_admin_email(name=name, phone=phone, email=email,subject =subject, message=message)

        # Send the response email to the dashboard
        send_user_response_email(name=name, phone=phone, email=email,subject =subject, message=message)


        return redirect(url_for('website_bp.contact'))
    else:
        # Form has errors
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Error in {field}: {error}', 'danger')

    return render_template('website/contact.html', form=form, current_year=CURRENT_YEAR, user=user)