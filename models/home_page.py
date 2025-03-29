from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy import String, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from flask_login import UserMixin

from . import db



class Home(db.Model):
    __tablename__ = 'HomePage'
    __table_args__ = {'schema': 'plumber_website'}

    id: Mapped[int] = mapped_column(primary_key=True)
    heading: Mapped[str] = mapped_column(String(2000), nullable=False)
    subheading: Mapped[str] = mapped_column(String(2000), nullable=False)
    description: Mapped[str] = mapped_column(String(2000), nullable=True)


    heading_two: Mapped[str] = mapped_column(String(2000), nullable=True)
    subheading_two: Mapped[str] = mapped_column(String(2000), nullable=True)
    description_two: Mapped[str] = mapped_column(String(2000), nullable=True)

    heading_three: Mapped[str] = mapped_column(String(2000), nullable=True)
    subheading_three: Mapped[str] = mapped_column(String(2000), nullable=True)
    description_three: Mapped[str] = mapped_column(String(2000), nullable=True)


    image_one: Mapped[str] = mapped_column(String(2000), nullable=True)
    image_two: Mapped[str] = mapped_column(String(2000), nullable=True)
    image_three: Mapped[str] = mapped_column(String(2000), nullable=True)
    image_four: Mapped[str] = mapped_column(String(2000), nullable=True)
    content_url_one: Mapped[str] = mapped_column(String(2000), nullable=True)
    content_url_two: Mapped[str] = mapped_column(String(2000), nullable=True)
    content_url_three: Mapped[str] = mapped_column(String(2000), nullable=True)
    def __repr__(self):
        return f'<HomePage{self.name}>'

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}