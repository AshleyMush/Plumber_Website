# models/__init__.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .dashboard import Services, CompanyDetails, Socials
from .home_page import Home
from .accredication import Accreditation
from .about_us import AboutUsPageContent
from .project_showcase import Jobs_Done, Reviewer, Service_Provider