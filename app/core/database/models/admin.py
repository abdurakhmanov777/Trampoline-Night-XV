"""
Модуль модели администратора.

Содержит ORM-модель администратора Telegram с полями для
идентификации, состояния, языка и текста сообщений.
"""

from typing import Any

from sqlalchemy import BigInteger, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Admin(Base):
    """ORM-модель администратора Telegram."""

    __tablename__: Any = "admin"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )
    tg_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False
    )
    bot_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False
    )
    _state: Mapped[str] = mapped_column(
        "state",
        String(32),
        nullable=False,
        default="1"
    )
    name: Mapped[str | None] = mapped_column(
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

    @property
    def state(self) -> list[str]:
        """Возвращает состояние как список."""
        if not self._state:
            return []
        return self._state.split(",")

    @state.setter
    def state(self, value: list[str]) -> None:
        """Устанавливает состояние списком."""
        self._state = ",".join(value)

    def push_state(self, value: str) -> None:
        """Положить элемент в стек состояния."""
        s: list[str] = self.state
        s.append(value)
        self.state = s

    def pop_state(self) -> str | None:
        """Снять элемент со стека состояния."""
        s: list[str] = self.state
        if not s:
            return None
        last: str = s.pop()
        self.state = s
        return last

    def peek_state(self) -> str | None:
        """Получить верхний элемент стека без удаления."""
        s: list[str] = self.state
        return s[-1] if s else None
    def __repr__(self) -> str:
        """Возвращает строковое представление администратора.

        Returns:
            str: Строка с идентификатором и tg_id администратора.
        """
        return f"<Admin id={self.id} tg_id={self.tg_id}>"
