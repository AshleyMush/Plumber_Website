from . import website_bp
from forms import ContactUSForm
from flask import render_template, flash, url_for, redirect
from utils.email_utils import send_admin_email, send_user_response_email
from models import db, User, Home, CompanyDetails, Socials, Services, Jobs_Done
import bleach # For sanitizing HTML
from datetime import datetime


CURRENT_YEAR = datetime.now().year



@website_bp.route('/gallery', methods=['GET','POST'] )
def gallery():
    user = User.query.first()
    form = ContactUSForm()
    company = CompanyDetails.query.first()
    jobs = Jobs_Done.query.all()
    socials = Socials.query.first()
    services = Services.query.all()


    return render_template('website/gallery.html',user=user,form =form, current_year=CURRENT_YEAR, company=company, socials=socials, jobs=jobs, services=services)