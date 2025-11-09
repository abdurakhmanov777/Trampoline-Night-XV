"""Модель пользователя Telegram."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, Optional

from sqlalchemy import BigInteger, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .data import Data  # Тип используется только для подсказок IDE


class User(Base):
    """Модель пользователя Telegram."""

    __tablename__: Any = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        unique=True
    )
    state: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default="1"
    )
    fullname: Mapped[Optional[str]] = mapped_column(
        String(255)
    )
    group: Mapped[Optional[str]] = mapped_column(
        String(255)
    )
    lang: Mapped[str] = mapped_column(
        String(8),
        nullable=False,
        default="ru"
    )
    msg_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )
    column: Mapped[Optional[int]] = mapped_column(Integer)
    date_registration: Mapped[Optional[datetime]] = mapped_column(
        DateTime
    )
    date_confirm: Mapped[Optional[datetime]] = mapped_column(
        DateTime
    )

    # Связь с таблицей Data
    data: Mapped[list[Data]] = relationship(
        "Data",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        """Строковое представление пользователя."""
        return f"<User id={self.id} tg_id={self.tg_id}>"
