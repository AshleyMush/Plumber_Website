from . import website_bp
from forms import ContactUSForm
from flask import render_template, flash, url_for, redirect
from utils.email_utils import send_admin_email, send_user_response_email
from models import db, User, Experience, Education, Skills, Language, Projects, Home
import bleach # For sanitizing HTML
from datetime import datetime


CURRENT_YEAR = datetime.now().year



@website_bp.route('/', methods=['GET'] )
def home():
    home = Home.query.first()
    user = User.query.first()
    form = ContactUSForm()


    return render_template('website/index.html',user=user, home=home,form =form, current_year=CURRENT_YEAR)