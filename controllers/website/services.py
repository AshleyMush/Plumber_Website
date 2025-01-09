from . import website_bp
from forms import ContactUSForm
from flask import render_template, flash, url_for, redirect
from utils.email_utils import send_admin_email, send_user_response_email
from models import db, User, Services, CompanyDetails, Socials
import bleach # For sanitizing HTML
from datetime import datetime


CURRENT_YEAR = datetime.now().year



@website_bp.route('/placeholder-service', methods=['GET','POST'] )
def get_placeholder_service():
    services = Services.query.all()
    company = CompanyDetails.query.first()
    socials = Socials.query.first()


    form = ContactUSForm()
    return render_template('website/service.html', form=form, services=services,current_year=CURRENT_YEAR, company=company, socials=socials, form_class="p-4 p-md-5 border rounded-3 bg-body-tertiary")

@website_bp.route('/service/<int:service_id>', methods=['GET','POST'] )
def get_service(service_id):
    services = Services.query.all()

    service = Services.query.get(service_id)
    form = ContactUSForm()
    return render_template('website/service.html', form=form, services=services,service=service,current_year=CURRENT_YEAR,form_class="p-4 p-md-5 border rounded-3 bg-body-tertiary")