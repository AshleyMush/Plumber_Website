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
    homeImage: Mapped[str] = mapped_column(String(2000), nullable=True)
    homeDescription: Mapped[str] = mapped_column(String(2000), nullable=True)
    description: Mapped[str] = mapped_column(String(2000), nullable=True)

    def __repr__(self):
        return f'<Services{self.title}>'

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


class CompanyDetails (db.Model):
    __tablename__ = 'CompanyDetails'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(2000), nullable=False)
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


class HomePage(db.Model):
    __tablename__ = 'HomePage'
    id: Mapped[int] = mapped_column(primary_key=True)
    heading: Mapped[str] = mapped_column(String(2000), nullable=False)
    subheading: Mapped[str] = mapped_column(String(2000), nullable=True)

    def __repr__(self):
        return f'<HomePage{self.name}>'

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class AboutUs(db.Model):
    __tablename__ = 'AboutUs'
    id: Mapped[int] = mapped_column(primary_key=True)
    headerImage: Mapped[str] = mapped_column(String(2000), nullable=True)
    description: Mapped[str] = mapped_column(String(2000), nullable=True)


class Socials (db.Model ):
    __tablename__ = 'Socials'
    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[str] = mapped_column(String(2000), nullable=False)
    instagram : Mapped[str] = mapped_column(String(2000), nullable=True)
    youtube : Mapped[str] = mapped_column(String(2000), nullable=True)
    facebook : Mapped[str] = mapped_column(String(2000), nullable=True)
    email : Mapped[str] = mapped_column(String(2000), nullable=True)

    def __repr__(self):
        return f'<Socials{self.name}>'

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


class Accreditation(db.Model):
    __tablename__ = 'accreditation'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(2000), nullable=False)
    image: Mapped[str] = mapped_column(String(2000), nullable=True)
    description: Mapped[str] = mapped_column(String(2000), nullable=True)

    def __repr__(self):
        return f'<accreditation{self.name}>'

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


class Reviewer (db.Model):
    __tablename__ = 'Reviewer'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(2000), nullable=False)
    review: Mapped[str] = mapped_column(String(2000), nullable=True)

    def __repr__(self):
        return f'<Reviewer{self.name}>'

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}