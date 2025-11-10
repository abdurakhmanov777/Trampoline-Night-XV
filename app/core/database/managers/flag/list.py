"""
Получение списка всех флагов.
"""

from typing import Sequence, Tuple

from sqlalchemy import Result, select
from sqlalchemy.exc import SQLAlchemyError

from app.core.database.models import Flag

from .base import FlagManagerBase


class FlagList(FlagManagerBase):
    """Класс для получения всех флагов из базы."""

    async def list_all(self) -> Sequence[Flag]:
        """
        Получить список всех флагов.
        """
        try:
            result: Result[Tuple[Flag]] = await self.session.execute(
                select(Flag)
            )
            return result.scalars().all()
        except SQLAlchemyError as e:
            print(f"Ошибка при получении списка флагов: {e}")
            return []
