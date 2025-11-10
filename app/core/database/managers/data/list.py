"""
Получение всех записей пользователя из таблицы Data.
"""

from typing import Sequence, Tuple

from sqlalchemy import Result, select
from sqlalchemy.exc import SQLAlchemyError

from app.core.database.models import Data

from .base import DataManagerBase


class DataList(DataManagerBase):
    """Класс для получения списка пар ключ–значение пользователя."""

    async def list_all(
        self,
        user_id: int
    ) -> Sequence[Data]:
        """
        Получить все пары ключ–значение для пользователя.
        """
        try:
            result: Result[Tuple[Data]] = await self.session.execute(
                select(Data).where(Data.user_id == user_id)
            )
            return result.scalars().all()
        except SQLAlchemyError as e:
            print(f"Ошибка при получении списка данных: {e}")
            return []
