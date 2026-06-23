from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base
from sqlalchemy import BigInteger, Integer
from datetime import datetime


class Clan(Base):
    __tablename__ = "clans"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger)
    title: Mapped[str]
    name: Mapped[str]
    tg_tag: Mapped[str] = mapped_column(nullable=True)
    photo: Mapped[str] = mapped_column(nullable=True)
    level: Mapped[str] = mapped_column(default=1)
    language: Mapped[str]
    sieges_league: Mapped[int] = mapped_column(nullable=True)
    requirements_hydra: Mapped[int] = mapped_column(nullable=True)
    requirements_himera: Mapped[int] = mapped_column(nullable=True)
    requirements_lkv: Mapped[int] = mapped_column(nullable=True)
    clan_tag: Mapped[str]

    is_published: Mapped[bool] = mapped_column(default=False, nullable=True)
    expiration_date: Mapped[datetime] = mapped_column(nullable=True)

    reviews = relationship("Review", back_populates="clan")