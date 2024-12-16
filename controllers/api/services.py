from . import api_bp
from flask import render_template, flash, url_for, redirect, jsonify
from models import db, User,  Home, Services
import bleach # For sanitizing HTML
from datetime import datetime


CURRENT_YEAR = datetime.now().year



@api_bp.route('/service/<int:service_id>', methods=['GET','POST'] )
def service(service_id):
    selected_service = Services.query.get(service_id)
    services = Services.query.all()
    if selected_service is None:
        return jsonify({"Empty": "No service content yet"}), 404

    if not services:
        return jsonify({"Empty": "No services content yet"}), 404

    selected_service_dict = selected_service.to_dict()
    services_dict = [service.to_dict() for service in services]

    return jsonify({"selected_service": selected_service_dict, "services": services_dict}), 200

