from . import api_bp
from flask import jsonify
from forms import ContactUSForm
from flask import render_template, flash, url_for, redirect
from utils.email_utils import send_admin_email, send_user_response_email
from models import db, User, Home, Services, Accreditation
import bleach # For sanitizing HTML
from datetime import datetime


CURRENT_YEAR = datetime.now().year



@api_bp.route('/home', methods=['GET'])
def home():
    home = Home.query.first()
    services = Services.query.all()

    if home is None:
        return jsonify({"Empty": "No home content yet"}), 404

    if not services:
        return jsonify({"Empty": "No services content yet"}), 404

    home_dict = home.to_dict()
    services_dict = [service.to_dict() for service in services]

    return jsonify({"home": home_dict, "services": services_dict}), 200