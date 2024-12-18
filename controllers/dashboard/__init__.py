from flask import Blueprint

dashboard_bp = Blueprint(
    'dashboard_bp',
    __name__,
    template_folder='templates',
    static_folder='static',
    url_prefix='/dashboard'

)

from . import user_profile_routes, services_routes,\
    company_profile_routes, home_page_routes,\
    accreditation_routes, about_us_routes, jobs_done_routes
