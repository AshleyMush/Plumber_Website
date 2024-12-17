from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, Text
from flask_sqlalchemy import SQLAlchemy
from . import db


# class Service_Provider(db.Model):
#     __tablename__ = 'Service_Provider'
#
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     name: Mapped[str] = mapped_column(String(500), nullable=False)
#     email: Mapped[str] = mapped_column(String(1200), unique=True, nullable=False)
#     number: Mapped[str] = mapped_column(String(1200), nullable=True)
#     password: Mapped[str] = mapped_column(String(1200), nullable=False)
#     role: Mapped[str] = mapped_column(String(200), nullable=False)
#
#     # Relationship with Jobs_Done
#     Jobs_Done: Mapped[list["Jobs_Done"]] = relationship('Jobs_Done', back_populates='Service_Provider', cascade="all, delete-orphan")
#
#     def __repr__(self):
#         return f'<Service_Provider {self.name}>'

class Jobs_Done(db.Model):
    __tablename__ = 'Jobs_Done'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(1000), nullable=False)
    main_image_path: Mapped[str] = mapped_column(String(2000), nullable=True)
    image_one_path: Mapped[str] = mapped_column(String(2000), nullable=True)
    image_two_path: Mapped[str] = mapped_column(String(2000), nullable=True)

    description: Mapped[str] = mapped_column(Text, nullable=False)

    location: Mapped[str] = mapped_column(String(2550), nullable=False)

    # Foreign Key linking to Service_Provider
    User_id: Mapped[int] = mapped_column(Integer, ForeignKey('User.id'), nullable=False)

    # Relationship with Reviewer
    reviews: Mapped[list["Reviewer"]] = relationship('Reviewer', back_populates='job', cascade="all, delete-orphan")

    # Relationship back to Service_Provider
    User: Mapped["User"] = relationship('User', back_populates='Jobs_Done')

    def __repr__(self):
        return f'<Jobs_Done {self.name}>'

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class Reviewer(db.Model):
    __tablename__ = 'reviews'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(2000), nullable=False)
    review: Mapped[str] = mapped_column(Text, nullable=False)

    # Foreign Key linking to Jobs_Done
    job_id: Mapped[int] = mapped_column(Integer, ForeignKey('Jobs_Done.id'), nullable=False)

    # Relationship back to Jobs_Done
    job: Mapped["Jobs_Done"] = relationship('Jobs_Done', back_populates='reviews')

    def __repr__(self):
        return f'<Reviewer {self.name}>'

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
