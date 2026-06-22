from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base
from datetime import datetime
from sqlalchemy import BigInteger, ForeignKey


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    score: Mapped[int]
    text: Mapped[str]
    reviewer: Mapped[str] = mapped_column(nullable=True, default=None)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

    player_id: Mapped[int | None] = mapped_column(ForeignKey("players.id"), nullable=True)
    clan_id: Mapped[int | None] = mapped_column(ForeignKey("clans.id"), nullable=True)

    player = relationship("Player", back_populates="reviews")  # type: ignore
    clan = relationship("Clan", back_populates="reviews")  # type: ignore