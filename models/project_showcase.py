from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, Text
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Plumber(db.Model):
    __tablename__ = 'plumber'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(500), nullable=False)
    email: Mapped[str] = mapped_column(String(1200), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(1200), nullable=False)
    role: Mapped[str] = mapped_column(String(200), nullable=False)

    # Relationship with Project
    projects: Mapped[list["Project"]] = relationship('Project', back_populates='plumber', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Plumber {self.name}>'


class Project(db.Model):
    __tablename__ = 'project'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(1000), nullable=False)
    image: Mapped[str] = mapped_column(String(2550), nullable=True)
    location: Mapped[str] = mapped_column(String(2550), nullable=False)

    # Foreign Key linking to Plumber
    plumber_id: Mapped[int] = mapped_column(Integer, ForeignKey('plumber.id'), nullable=False)

    # Relationship with Reviewer
    reviews: Mapped[list["Reviewer"]] = relationship('Reviewer', back_populates='project', cascade="all, delete-orphan")

    # Relationship back to Plumber
    plumber: Mapped["Plumber"] = relationship('Plumber', back_populates='projects')

    def __repr__(self):
        return f'<Project {self.name}>'


class Reviewer(db.Model):
    __tablename__ = 'reviewer'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(2000), nullable=False)
    review: Mapped[str] = mapped_column(Text, nullable=False)

    # Foreign Key linking to Project
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey('project.id'), nullable=False)

    # Relationship back to Project
    project: Mapped["Project"] = relationship('Project', back_populates='reviews')

    def __repr__(self):
        return f'<Reviewer {self.name}>'
