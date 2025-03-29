from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy import String, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from flask_login import UserMixin

from . import db




class Accreditation(db.Model):
    __tablename__ = 'Accreditation'
    __table_args__ = {'schema': 'plumber_website'}

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(2000), nullable=False)
    image: Mapped[str] = mapped_column(String(2000), nullable=True)
    description: Mapped[str] = mapped_column(String(2000), nullable=True)

    def __repr__(self):
        return f'<accreditation{self.name}>'

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


