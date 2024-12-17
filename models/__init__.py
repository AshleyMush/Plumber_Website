# models/__init__.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .dashboard import Services, CompanyDetails, Socials
from .home_page import Home
from .accredication import Accreditation
from .about_us import AboutUsPageContent

from .user import User
from .project_showcase import Jobs_Done, Reviewer