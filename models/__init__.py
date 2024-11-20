# models/__init__.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .portfolio import Experience, Projects, Skills, Education, Language
from .user import User
from .dashboard import Services, CompanyDetails, Socials
from .project_showcase import Plumber, Job, Reviewer
from .home_page import Home
from .accredication import Accreditation
from .about_us import AboutUsPageContent