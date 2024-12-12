from . import website_bp
from forms import ContactUSForm
from flask import render_template, flash, url_for, redirect
from utils.email_utils import send_admin_email, send_user_response_email
from models import db, User,  Home
import bleach # For sanitizing HTML
from datetime import datetime


CURRENT_YEAR = datetime.now().year



@website_bp.route('/service', methods=['GET','POST'] )
def service():

    form = ContactUSForm()
    return render_template('website/service.html', form=form, current_year=CURRENT_YEAR)