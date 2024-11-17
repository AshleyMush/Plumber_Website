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
        return f'<Services {self.name}>'

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}







class AboutUsPageContent(db.Model):
    __tablename__ = 'AboutUsContent'
    id: Mapped[int] = mapped_column(primary_key=True)
    headerImage: Mapped[str] = mapped_column(String(2000), nullable=True)
    description: Mapped[str] = mapped_column(String(2000), nullable=True)






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
