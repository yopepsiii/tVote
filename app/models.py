from datetime import datetime
import uuid

from sqlalchemy import func, types, text, ForeignKey, select
from sqlalchemy.orm import (
    declarative_base,
    Mapped,
    mapped_column,
    relationship,
    column_property,
)

Base = declarative_base()


class User(Base):
    __tablename__ = "Users"

    id: Mapped[uuid.UUID] = mapped_column(
        types.Uuid, server_default=text("gen_random_uuid()"), primary_key=True
    )

    firstname: Mapped[str] = mapped_column(nullable=False)
    surname: Mapped[str] = mapped_column(nullable=False)

    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, server_default=func.now()
    )

    votes: Mapped[list["Vote"]] = relationship(cascade="all, delete-orphan")
    profburo_vote: Mapped['ProfburoVote'] = relationship(cascade="all, delete-orphan")


class Vote(Base):
    __tablename__ = "Votes"

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("Users.id", ondelete="CASCADE"), primary_key=True
    )

    candidate_id: Mapped[int] = mapped_column(
        ForeignKey("Candidates.id", ondelete="CASCADE"), primary_key=True
    )

    type: Mapped[int] = mapped_column(nullable=False)


class ProfburoVote(Base):
    __tablename__ = "ProfburoVotes"

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("Users.id", ondelete="CASCADE"), primary_key=True
    )

    type: Mapped[int] = mapped_column(nullable=False)


class Candidate(Base):
    __tablename__ = "Candidates"

    id: Mapped[int] = mapped_column(primary_key=True)

    firstname: Mapped[str] = mapped_column(nullable=False)
    surname: Mapped[str] = mapped_column()

    year_of_study: Mapped[int] = mapped_column()
    group: Mapped[str] = mapped_column()
    study_dirrection: Mapped[str] = mapped_column()

    photo: Mapped[str] = mapped_column()

    likes_count = column_property(
        select(func.count(Vote.candidate_id))
        .where((Vote.candidate_id == id) & (Vote.type == 1))
        .correlate_except(Vote)
        .scalar_subquery()
    )
    dislikes_count: Mapped[int] = column_property(
        select(func.count(Vote.candidate_id))
        .where((Vote.candidate_id == id) & (Vote.type == 0))
        .correlate_except(Vote)
        .scalar_subquery()
    )

    abstaines_count: Mapped[int] = column_property(
        select(func.count(Vote.candidate_id))
        .where((Vote.candidate_id == id) & (Vote.type == 2))
        .correlate_except(Vote)
        .scalar_subquery()
    )


class ProfburoMember(Base):
    __tablename__ = "ProfburoMembers"

    id: Mapped[int] = mapped_column(primary_key=True)

    firstname: Mapped[str] = mapped_column(nullable=False)
    surname: Mapped[str] = mapped_column(nullable=False)

    info: Mapped[str] = mapped_column(nullable=True)
    direction: Mapped[str] = mapped_column(nullable=True)

    photo: Mapped[str] = mapped_column(nullable=False)


class Admin(Base):
    __tablename__ = "Admins"

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("Users.id", ondelete="CASCADE"), primary_key=True
    )
    user: Mapped["User"] = relationship(foreign_keys=user_id)
