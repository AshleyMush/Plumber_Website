from . import api_bp
from flask import  jsonify
from utils.email_utils import send_admin_email, send_user_response_email
from models import db, User, Socials, CompanyDetails
import bleach # For sanitizing HTML
from datetime import datetime


CURRENT_YEAR = datetime.now().year



@api_bp.route('/contact-us', methods=['GET'])
def contact():
    socials = Socials.query.first()
    company_details = CompanyDetails.query.first()

    if socials is None:
        return jsonify({"Empty": "No socials content yet"}), 404

    if company_details is None:
        return jsonify({"Empty": "No company details content yet"}), 404

    socials_dict = socials.to_dict()
    company_details_dict = company_details.to_dict()

    return jsonify({"socials": socials_dict, "company_details": company_details_dict}), 200
