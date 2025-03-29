from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy import String, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from flask_login import UserMixin

from . import db




class AboutUsPageContent(db.Model):
    __tablename__ = 'AboutUsContent'
    __table_args__ = {'schema': 'plumber_website'}

    id: Mapped[int] = mapped_column(primary_key=True)
    heading: Mapped[str] = mapped_column(String(2000), nullable=False)
    subheading: Mapped[str] = mapped_column(String(2000), nullable=False)

    main_image_path: Mapped[str] = mapped_column(String(2000), nullable=True)
    image_one_path: Mapped[str] = mapped_column(String(2000), nullable=True)
    image_two_path: Mapped[str] = mapped_column(String(2000), nullable=True)

    content_one_url: Mapped[str] = mapped_column(String(2000), nullable=True)
    content_two_url: Mapped[str] = mapped_column(String(2000), nullable=True)
    content_three_url: Mapped[str] = mapped_column(String(2000), nullable=True)

    feature_one_heading: Mapped[str] = mapped_column(String(2000), nullable=True)
    feature_one_description: Mapped[str] = mapped_column(String(2000), nullable=True)
    feature_two_heading: Mapped[str] = mapped_column(String(2000), nullable=True)
    feature_two_description: Mapped[str] = mapped_column(String(2000), nullable=True)


def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


