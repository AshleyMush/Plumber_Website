from . import api_bp
from flask import jsonify
from forms import ContactUSForm
from flask import render_template, flash, url_for, redirect
from utils.email_utils import send_admin_email, send_user_response_email
from models import db, User, Home
import bleach # For sanitizing HTML
from datetime import datetime


CURRENT_YEAR = datetime.now().year



@api_bp.route('/home', methods=['GET'] )
def home():
    home = Home.query.first()







    home_dict = home.to_dict()


    return jsonify()