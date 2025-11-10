"""
CRUD-операции для таблицы Flag.
"""

from typing import Optional, Tuple

from sqlalchemy import Result, select
from sqlalchemy.exc import SQLAlchemyError

from app.core.database.models import Flag

from .base import FlagManagerBase


class FlagCRUD(FlagManagerBase):
    """Класс для выполнения CRUD-операций с флагами."""

    async def get(
        self,
        name: str
    ) -> Optional[Flag]:
        """
        Получить флаг по имени.
        """
        try:
            result: Result[Tuple[Flag]] = await self.session.execute(
                select(Flag).where(Flag.name == name)
            )
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            print(f"Ошибка при получении флага: {e}")
            return None

    async def create(
        self,
        name: str,
        value: bool = False
    ) -> Flag:
        """
        Создать новый флаг.
        """
        flag = Flag(name=name, value=value)
        self.session.add(flag)
        await self.session.commit()
        await self.session.refresh(flag)
        return flag

    async def update(
        self,
        name: str,
        value: bool
    ) -> bool:
        """
        Обновить значение флага.
        """
        flag: Optional[Flag] = await self.get(name)
        if not flag:
            return False

        flag.value = value
        await self.session.commit()
        return True

    async def delete(
        self,
        name: str
    ) -> bool:
        """
        Удалить флаг по имени.
        """
        flag: Optional[Flag] = await self.get(name)
        if not flag:
            return False

        await self.session.delete(flag)
        await self.session.commit()
        return True
