# app/models.py
from datetime import datetime as py_datetime, date as py_date, time as py_time
from typing import List, Optional
from sqlalchemy import (
    ForeignKey,
    Text,
    String,
    Integer,
    Boolean,
    BigInteger,
    Time,
    DateTime,
    Date,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .__init__ import db


class Team(db.Model):
    __tablename__ = "team"
    id: Mapped[int] = mapped_column(primary_key=True)
    team_name: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[py_datetime] = mapped_column(
        DateTime, default=py_datetime.utcnow
    )

    members: Mapped[List["Member"]] = relationship(back_populates="team")
    sprints: Mapped[List["Sprint"]] = relationship(back_populates="team")
    settings: Mapped["TeamSettings"] = relationship(
        back_populates="team", uselist=False
    )
    daily_sessions: Mapped[List["DailySession"]] = relationship(back_populates="team")


class Member(db.Model):
    __tablename__ = "member"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(100))
    discord_id: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    team_id: Mapped[Optional[int]] = mapped_column(ForeignKey("team.id"), nullable=True)
    created_at: Mapped[py_datetime] = mapped_column(
        DateTime, default=py_datetime.utcnow
    )

    team: Mapped["Team"] = relationship(back_populates="members")
    answers: Mapped[List["Answer"]] = relationship(back_populates="member")
    commitments: Mapped[List["Commitment"]] = relationship(back_populates="member")
    voice_logs: Mapped[List["VoiceChannelLog"]] = relationship(back_populates="member")


class Sprint(db.Model):
    __tablename__ = "sprint"
    id: Mapped[int] = mapped_column(primary_key=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("team.id"), nullable=False)
    start_date: Mapped[py_date] = mapped_column(Date, nullable=False)
    end_date: Mapped[py_date] = mapped_column(Date, nullable=False)
    created_at: Mapped[py_datetime] = mapped_column(
        DateTime, default=py_datetime.utcnow
    )

    team: Mapped["Team"] = relationship(back_populates="sprints")
    commitments: Mapped[List["Commitment"]] = relationship(back_populates="sprint")


class Commitment(db.Model):
    __tablename__ = "commitment"
    id: Mapped[int] = mapped_column(primary_key=True)
    sprint_id: Mapped[int] = mapped_column(ForeignKey("sprint.id"), nullable=False)
    member_id: Mapped[int] = mapped_column(ForeignKey("member.id"), nullable=False)
    commitment_description: Mapped[str] = mapped_column(Text, nullable=False)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[py_datetime] = mapped_column(
        DateTime, default=py_datetime.utcnow
    )

    sprint: Mapped["Sprint"] = relationship(back_populates="commitments")
    member: Mapped["Member"] = relationship(back_populates="commitments")
    checklists: Mapped[List["Checklist"]] = relationship(back_populates="commitment")


class Checklist(db.Model):
    __tablename__ = "checklist"
    id: Mapped[int] = mapped_column(primary_key=True)
    commitment_id: Mapped[int] = mapped_column(
        ForeignKey("commitment.id"), nullable=False
    )
    check_date: Mapped[py_date] = mapped_column(
        Date, nullable=False, default=py_date.today
    )
    status: Mapped[bool] = mapped_column(Boolean, default=False)

    commitment: Mapped["Commitment"] = relationship(back_populates="checklists")


class VoiceChannelLog(db.Model):
    __tablename__ = "voice_channel_log"
    id: Mapped[int] = mapped_column(primary_key=True)
    member_id: Mapped[int] = mapped_column(ForeignKey("member.id"), nullable=False)
    channel_name: Mapped[str] = mapped_column(String(100), nullable=False)
    joined_at: Mapped[py_datetime] = mapped_column(DateTime, nullable=False)
    left_at: Mapped[Optional[py_datetime]] = mapped_column(DateTime, nullable=True)

    member: Mapped["Member"] = relationship(back_populates="voice_logs")


class Question(db.Model):
    __tablename__ = "question"
    id: Mapped[int] = mapped_column(primary_key=True)
    question_text: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[py_datetime] = mapped_column(
        DateTime, default=py_datetime.utcnow
    )

    answers: Mapped[List["Answer"]] = relationship(back_populates="question")


class Answer(db.Model):
    __tablename__ = "answer"
    id: Mapped[int] = mapped_column(primary_key=True)
    question_id: Mapped[int] = mapped_column(ForeignKey("question.id"), nullable=False)
    member_id: Mapped[int] = mapped_column(ForeignKey("member.id"), nullable=False)
    answer_text: Mapped[str] = mapped_column(Text, nullable=False)
    answered_at: Mapped[py_datetime] = mapped_column(
        DateTime, default=py_datetime.utcnow
    )

    question: Mapped["Question"] = relationship(back_populates="answers")
    member: Mapped["Member"] = relationship(back_populates="answers")


class DailySession(db.Model):
    __tablename__ = "daily_session"
    id: Mapped[int] = mapped_column(primary_key=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("team.id"), nullable=False)
    date: Mapped[py_date] = mapped_column(Date, nullable=False, default=py_date.today)
    is_closed: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[py_datetime] = mapped_column(
        DateTime, default=py_datetime.utcnow
    )

    team: Mapped["Team"] = relationship(back_populates="daily_sessions")


class TeamSettings(db.Model):
    __tablename__ = "team_settings"

    id: Mapped[int] = mapped_column(primary_key=True)
    team_id: Mapped[int] = mapped_column(
        ForeignKey("team.id"), unique=True, nullable=False
    )

    # daily_time is a Python time, stored as a SQL Time
    daily_time: Mapped[py_time] = mapped_column(Time, nullable=False)

    # reminder_interval is an integer, stored as an Integer column
    reminder_interval: Mapped[int] = mapped_column(Integer, default=24)

    # channel_id is a Python int, stored as BigInteger
    channel_id: Mapped[int] = mapped_column(BigInteger, nullable=False)

    # date / time fields can use:
    # created_at: Mapped[py_datetime] = mapped_column(DateTime, default=py_datetime.utcnow)

    team: Mapped["Team"] = relationship(back_populates="settings")
