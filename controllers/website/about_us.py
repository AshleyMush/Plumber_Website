from . import website_bp
from forms import ContactUSForm
from flask import render_template, flash, url_for, redirect
from utils.email_utils import send_admin_email, send_user_response_email
from models import db, User, Home, CompanyDetails, Socials, AboutUsPageContent, Services,Jobs_Done
import bleach # For sanitizing HTML
from datetime import datetime


CURRENT_YEAR = datetime.now().year


@website_bp.route('/about-us', methods=['GET', 'POST'] )
def about_us():
    company = CompanyDetails.query.first()
    socials = Socials.query.first()
    about= AboutUsPageContent.query.first()
    services = Services.query.all()
    jobs = Jobs_Done.query.all()


    return render_template('website/about.html', current_year=CURRENT_YEAR, company=company, socials=socials, about=about, services=services, jobs=jobs)