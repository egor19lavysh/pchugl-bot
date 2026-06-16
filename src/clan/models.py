from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base
from sqlalchemy import BigInteger
from datetime import datetime

class Clan(Base):
    __tablename__ = "clans"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger)
    title: Mapped[str]
    name: Mapped[str]
    tg_tag: Mapped[str] = mapped_column(nullable=True)
    photo: Mapped[str] = mapped_column(nullable=True)
    level: Mapped[str] = mapped_column(default=1)
    language: Mapped[str]
    sieges_league: Mapped[str]
    requirements_hydra: Mapped[str]
    requirements_himera: Mapped[str]
    requirements_lkv: Mapped[str]

    is_published: Mapped[bool] = mapped_column(default=False, nullable=True)
    expiration_date: Mapped[datetime] = mapped_column(nullable=True)