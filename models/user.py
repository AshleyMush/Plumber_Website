from flask_login import UserMixin
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import String, Integer

from . import db

class User(db.Model, UserMixin):
    __tablename__ = "User"
    __table_args__ = {'schema': 'plumber_website'}

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(2000), nullable=True)
    password: Mapped[str] = mapped_column(String(2000), nullable=False)
    first_name: Mapped[str] = mapped_column(String(2000), nullable=False)
    last_name: Mapped[str] = mapped_column(String(2000), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(2000), nullable=True)
    about: Mapped[str] = mapped_column(String(2000), nullable=True)
    github_url: Mapped[str] = mapped_column(String(2000), nullable=True)
    linkedin_url: Mapped[str] = mapped_column(String(2000), nullable=True)
    facebook_url: Mapped[str] = mapped_column(String(2000), nullable=True)
    instagram_url: Mapped[str] = mapped_column(String(2000), nullable=True)
    hackerrank_url: Mapped[str] = mapped_column(String(2000), nullable=True)
    role: Mapped[str] = mapped_column(String(1000), nullable=False, default='User')

    # Use string references to avoid circular imports
    jobs_done: Mapped[list["Jobs_Done"]] = relationship(
        "Jobs_Done",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f'<User {self.email}>'

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}