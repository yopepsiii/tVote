from datetime import datetime
import uuid

from sqlalchemy import func, types, text, ForeignKey, select
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship, column_property

Base = declarative_base()


class User(Base):
    __tablename__ = 'Users'

    id: Mapped[uuid.UUID] = mapped_column(types.Uuid, server_default=text("gen_random_uuid()"), primary_key=True)

    firstname: Mapped[str] = mapped_column(nullable=False)
    surname: Mapped[str] = mapped_column(nullable=False)

    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False, server_default=func.now())

    votes: Mapped[list['Vote']] = relationship(back_populates='user')


class Vote(Base):
    __tablename__ = 'Votes'

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('Users.id', ondelete="CASCADE"), primary_key=True)
    user: Mapped['User'] = relationship(back_populates='votes', single_parent=True)

    candidate_id: Mapped[int] = mapped_column(ForeignKey('Candidates.id', ondelete="CASCADE"), primary_key=True)

    type: Mapped[int] = mapped_column(nullable=False)


class Candidate(Base):
    __tablename__ = 'Candidates'

    id: Mapped[int] = mapped_column(primary_key=True)

    firstname: Mapped[str] = mapped_column(nullable=False)
    surname: Mapped[str] = mapped_column(nullable=False)

    year_of_study: Mapped[int] = mapped_column(nullable=False)
    group: Mapped[str] = mapped_column(nullable=False)
    faculty: Mapped[str] = mapped_column(nullable=False)
    study_dirrection: Mapped[str] = mapped_column(nullable=False)

    photo: Mapped[str] = mapped_column(nullable=False)

    likes_count = column_property(
        select(func.count(Vote.candidate_id)).where(
            (Vote.candidate_id == id) & (Vote.type == 1)
        ).correlate_except(Vote)
        .scalar_subquery()
    )
    dislikes_count: Mapped[int] = column_property(
        select(func.count(Vote.candidate_id)).where(
            (Vote.candidate_id == id) & (Vote.type == 0)
        ).correlate_except(Vote)
        .scalar_subquery()
    )


class Admin(Base):
    __tablename__ = "Admins"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("Users.id", ondelete="CASCADE"), primary_key=True)
    user: Mapped['User'] = relationship(foreign_keys=user_id)
