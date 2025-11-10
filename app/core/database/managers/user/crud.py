"""
CRUD-операции для таблицы User.
"""

from typing import Optional, Tuple

from sqlalchemy import Result, select
from sqlalchemy.exc import SQLAlchemyError

from app.core.database.models import User

from .base import UserManagerBase


class UserCRUD(UserManagerBase):
    """Класс для CRUD-операций с пользователями."""

    async def get(self, tg_id: int) -> Optional[User]:
        """
        Получить пользователя по Telegram ID.
        """
        try:
            result: Result[Tuple[User]] = await self.session.execute(
                select(User).where(User.tg_id == tg_id)
            )
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            print(f"Ошибка при получении пользователя: {e}")
            return None

    async def create(
        self,
        tg_id: int,
        fullname: Optional[str] = None,
        group: Optional[str] = None,
        lang: str = "ru",
        msg_id: int = 0,
        column: Optional[int] = None,
    ) -> User:
        """
        Создать нового пользователя.
        """
        user = User(
            tg_id=tg_id,
            fullname=fullname,
            group=group,
            lang=lang,
            msg_id=msg_id,
            column=column,
            state="1",
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def delete(self, tg_id: int) -> bool:
        """
        Удалить пользователя из базы.
        """
        user: Optional[User] = await self.get(tg_id)
        if not user:
            return False

        await self.session.delete(user)
        await self.session.commit()
        return True
