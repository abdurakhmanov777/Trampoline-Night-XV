"""
Модель администратора.
"""

from typing import Any, Optional

from sqlalchemy import BigInteger, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Admin(Base):
    """Модель администратора Telegram."""

    __tablename__: Any = "admin"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False
    )
    state: Mapped[str] = mapped_column(
        String(32),
        default="1",
        nullable=False
    )
    name: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True
    )
    lang: Mapped[str] = mapped_column(
        String(8),
        default="ru",
        nullable=False
    )
    text: Mapped[str] = mapped_column(
        String,
        default="Нет текста",
        nullable=False
    )
    entities: Mapped[str] = mapped_column(
        String,
        default="None",
        nullable=False
    )
    msg_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    def __repr__(self) -> str:
        """Строковое представление администратора."""
        return f"<Admin id={self.id} tg_id={self.tg_id}>"
