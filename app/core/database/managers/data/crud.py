"""
CRUD-операции для работы с таблицей Data.
"""

from typing import Optional, Tuple

from sqlalchemy import Result, select
from sqlalchemy.exc import SQLAlchemyError

from app.core.database.models import Data

from .base import DataManagerBase


class DataCRUD(DataManagerBase):
    """Класс для выполнения CRUD-операций с данными пользователей."""

    async def get(
        self,
        user_id: int,
        key: str
    ) -> Optional[Data]:
        """
        Получить запись по ключу для конкретного пользователя.
        """
        try:
            result: Result[Tuple[Data]] = await self.session.execute(
                select(Data).where(
                    Data.user_id == user_id,
                    Data.key == key
                )
            )
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            print(f"Ошибка при получении данных: {e}")
            return None

    async def create(
        self,
        user_id: int,
        key: str,
        value: str
    ) -> Data:
        """
        Создать новую пару ключ–значение.
        """
        data = Data(
            user_id=user_id,
            key=key,
            value=value
        )
        self.session.add(data)
        await self.session.commit()
        await self.session.refresh(data)
        return data

    async def update(
        self,
        user_id: int,
        key: str,
        value: str
    ) -> bool:
        """
        Обновить значение существующего ключа.
        """
        data: Optional[Data] = await self.get(user_id, key)
        if not data:
            return False

        data.value = value
        await self.session.commit()
        return True

    async def delete(
        self,
        user_id: int,
        key: str
    ) -> bool:
        """
        Удалить пару ключ–значение пользователя.
        """
        data: Optional[Data] = await self.get(user_id, key)
        if not data:
            return False

        await self.session.delete(data)
        await self.session.commit()
        return True
