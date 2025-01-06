from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy import String, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from flask_login import UserMixin

from . import db








class Services(db.Model):
    __tablename__ = 'Services'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(2000), nullable=False)
    home_page_card_text: Mapped[str] = mapped_column(String(2000), nullable=True)

    main_image_path: Mapped[str] = mapped_column(String(2000), nullable=True)
    image_one_path: Mapped[str] = mapped_column(String(2000), nullable=True)
    image_two_path: Mapped[str] = mapped_column(String(2000), nullable=True)

    content_one_url: Mapped[str] = mapped_column(String(2000), nullable=True)
    content_two_url: Mapped[str] = mapped_column(String(2000), nullable=True)
    content_three_url: Mapped[str] = mapped_column(String(2000), nullable=True)

    header_description: Mapped[str] = mapped_column(String(2000), nullable=True)
    feature_heading_one: Mapped[str] = mapped_column(String(2000), nullable=True)
    feature_description_one: Mapped[str] = mapped_column(String(2000), nullable=True)
    feature_heading_two: Mapped[str] = mapped_column(String(2000), nullable=True)
    feature_description_two: Mapped[str] = mapped_column(String(2000), nullable=True)

    service_page_ckd_description: Mapped[str] = mapped_column(String(2000), nullable=True)
    icon_class : Mapped[str] = mapped_column(String(250))  # For both Bootstrap and Font Awesome classes






    def __repr__(self):
        return f'<Services {self.name}>'

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}











class CompanyDetails (db.Model):
    __tablename__ = 'CompanyDetails'
    id: Mapped[int] = mapped_column(primary_key=True)

# TODO: Add email ,phone and any missing columns to the company_routes.py
    name: Mapped[str] = mapped_column(String(2000), nullable=True)
    email : Mapped[str] = mapped_column(String(2000), nullable=True)

    phone : Mapped[str] = mapped_column(String(2000), nullable=True)

    logo: Mapped[str] = mapped_column(String(2000), nullable=True)
    address: Mapped[str] = mapped_column(String(2000), nullable=True)
    motto: Mapped[str] = mapped_column(String(2000), nullable=True)
    about : Mapped[str] = mapped_column(String(2000), nullable=True)
    openingHours: Mapped[str] = mapped_column(String(2000), nullable=True)
    weekendHours: Mapped[str] = mapped_column(String(2000), nullable=True)

    def __repr__(self):
        return f'<CompanyDetails{self.title}>'

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


class Socials (db.Model ):
    __tablename__ = 'Socials'
    id: Mapped[int] = mapped_column(primary_key=True)
    instagram : Mapped[str] = mapped_column(String(2000), nullable=True)
    whatsapp : Mapped[str] = mapped_column(String(2000), nullable=True)
    youtube : Mapped[str] = mapped_column(String(2000), nullable=True)
    facebook : Mapped[str] = mapped_column(String(2000), nullable=True)
    threads : Mapped[str] = mapped_column(String(2000), nullable=True)
    x : Mapped[str] = mapped_column(String(2000), nullable=True)

    def __repr__(self):
        return f'<Socials{self.name}>'

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
