from . import api_bp
from flask import jsonify
from models import db, User, AboutUsPageContent,Services,Accreditation
import bleach # For sanitizing HTML
from datetime import datetime


CURRENT_YEAR = datetime.now().year


@api_bp.route('/about-us', methods=['GET', 'POST'] )
def about_us():

    about_us = AboutUsPageContent.query.first()
    services = Services.query.all()
    accreditations = Accreditation.query.all()

    if about_us is None:
        return jsonify({"Empty": "No about us content yet"}), 404

    if not services:
        return jsonify({"Empty": "No services content yet"}), 404

    if not accreditations:
        return jsonify({"Empty": "No accreditations content yet"}), 404

    about_us_dict = about_us.to_dict()
    services_dict = [service.to_dict() for service in services]
    accreditations_dict = [accreditation.to_dict() for accreditation in accreditations]

    return jsonify({"about_us": about_us_dict, "services": services_dict, "accreditations": accreditations_dict}), 200