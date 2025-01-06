from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, Text

from . import db

class Jobs_Done(db.Model):
    __tablename__ = 'Jobs_Done'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(1000), nullable=False)
    image: Mapped[str] = mapped_column(String(2550), nullable=True)
    location: Mapped[str] = mapped_column(String(2550), nullable=False)

    # Explicitly name the foreign key constraint
    service_provider_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('User.id', name='fk_jobs_done_service_provider'),
        nullable=False
    )

    # Define relationships with back references
    reviews: Mapped[list["Reviewer"]] = relationship(
        "Reviewer",
        back_populates="job",
        cascade="all, delete-orphan"
    )
    user: Mapped["User"] = relationship("User", back_populates="jobs_done")

    def __repr__(self):
        return f'<Jobs_Done {self.name}>'

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


class Reviewer(db.Model):
    __tablename__ = 'reviews'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(2000), nullable=False)
    review: Mapped[str] = mapped_column(Text, nullable=False)

    job_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('Jobs_Done.id', name='fk_reviews_job_id'),
        nullable=False
    )

    job: Mapped["Jobs_Done"] = relationship("Jobs_Done", back_populates="reviews")

    def __repr__(self):
        return f'<Reviewer {self.name}>'

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
