"""
Получение всех записей пользователя из таблицы Data.

Содержит методы для получения списка всех пар ключ–значение
для конкретного пользователя.
"""

from typing import Sequence, Tuple

from loguru import logger
from sqlalchemy import Result, delete, select
from sqlalchemy.exc import SQLAlchemyError

from app.core.database.models import Data

from .base import DataManagerBase


class DataList(DataManagerBase):
    """Класс для получения списка пар ключ–значение пользователя."""

    async def list_all(
        self,
        tg_id: int,
    ) -> Sequence[Data]:
        """
        Получить все пары ключ–значение для пользователя.

        Args:
            tg_id (int): ID пользователя.

        Returns:
            Sequence[Data]: Список объектов Data пользователя.
        """
        try:
            result: Result[Tuple[Data]] = await self.session.execute(
                select(Data).where(Data.tg_id == tg_id)
            )
            # Возвращаем все записи пользователя
            return result.scalars().all()
        except SQLAlchemyError as e:
            # Логируем ошибку при получении списка данных
            logger.error(f"Ошибка при получении списка данных: {e}")
            return []

    async def clear_all(
        self,
        tg_id: int,
    ) -> bool:
        """
        Удалить все записи пользователя.

        Args:
            tg_id (int): ID пользователя.

        Returns:
            bool: True, если удаление прошло успешно, иначе False.
        """
        try:
            await self.session.execute(
                delete(Data).where(Data.tg_id == tg_id)
            )
            await self.session.commit()
            return True
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при удалении данных пользователя: {e}")
            await self.session.rollback()
            return False
