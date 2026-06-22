from __future__ import annotations

import src.fit.models  # noqa: F401
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base
from sqlalchemy import Integer, Date, ForeignKey, BigInteger, String
from sqlalchemy.dialects.postgresql import ARRAY
from datetime import datetime


class Player(Base):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger)
    title: Mapped[str]
    nickname: Mapped[str]
    tg_tag: Mapped[str] = mapped_column(nullable=True)
    level: Mapped[int] = mapped_column(default=1)
    account_strength: Mapped[int] = mapped_column(default=1)
    language: Mapped[str]
    sieges_league: Mapped[str]
    requirements_hydra: Mapped[str]
    requirements_himera: Mapped[str]
    requirements_lkv: Mapped[str]

    is_published: Mapped[bool] = mapped_column(default=False, nullable=True)
    expiration_date: Mapped[datetime] = mapped_column(nullable=True)

    reviews = relationship("Review", back_populates="player")