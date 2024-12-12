from flask import Blueprint

website_bp = Blueprint(
    'website_bp',
    __name__,
    template_folder='templates',
    static_folder='static',
)

from . import home, about_us,contact_us, services, review,gallery