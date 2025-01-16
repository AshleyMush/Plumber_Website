from . import website_bp
from forms import ContactUSForm
from flask import render_template, flash, url_for, redirect
from utils.email_utils import send_admin_email, send_user_response_email
from models import db, User, Home, Services, CompanyDetails, Socials, Jobs_Done
import bleach # For sanitizing HTML
from datetime import datetime


CURRENT_YEAR = datetime.now().year



@website_bp.route('/', methods=['GET'] )
def home():
    home = Home.query.first()
    user = User.query.first()
    form = ContactUSForm()
    services = Services.query.all()
    company = CompanyDetails.query.first()
    socials = Socials.query.first()
    jobs = Jobs_Done.query.all()




    return render_template('website/index.html',user=user, services=services,home=home,form =form, current_year=CURRENT_YEAR, company=company, socials=socials, jobs=jobs)