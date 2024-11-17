from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, Text
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Plumber(db.Model):
    __tablename__ = 'plumber'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(500), nullable=False)
    email: Mapped[str] = mapped_column(String(1200), unique=True, nullable=False)
    number: Mapped[str] = mapped_column(String(1200), nullable=True)
    password: Mapped[str] = mapped_column(String(1200), nullable=False)
    role: Mapped[str] = mapped_column(String(200), nullable=False)

    # Relationship with Job
    jobs: Mapped[list["Job"]] = relationship('Job', back_populates='plumber', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Plumber {self.name}>'

class Job(db.Model):
    __tablename__ = 'jobs'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(1000), nullable=False)
    image: Mapped[str] = mapped_column(String(2550), nullable=True)
    location: Mapped[str] = mapped_column(String(2550), nullable=False)

    # Foreign Key linking to Plumber
    plumber_id: Mapped[int] = mapped_column(Integer, ForeignKey('plumber.id'), nullable=False)

    # Relationship with Reviewer
    reviews: Mapped[list["Reviewer"]] = relationship('Reviewer', back_populates='job', cascade="all, delete-orphan")

    # Relationship back to Plumber
    plumber: Mapped["Plumber"] = relationship('Plumber', back_populates='jobs')

    def __repr__(self):
        return f'<Job {self.name}>'

class Reviewer(db.Model):
    __tablename__ = 'reviews'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(2000), nullable=False)
    review: Mapped[str] = mapped_column(Text, nullable=False)

    # Foreign Key linking to Job
    job_id: Mapped[int] = mapped_column(Integer, ForeignKey('jobs.id'), nullable=False)

    # Relationship back to Job
    job: Mapped["Job"] = relationship('Job', back_populates='reviews')

    def __repr__(self):
        return f'<Reviewer {self.name}>'
