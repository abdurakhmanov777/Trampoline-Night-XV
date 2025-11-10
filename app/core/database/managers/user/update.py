"""
Обновление полей пользователя.
"""

from typing import Optional

from app.core.database.models import User

from .crud import UserCRUD


class UserUpdate(UserCRUD):
    """Менеджер для обновления полей пользователя."""

    async def update_fullname(self, tg_id: int, fullname: str) -> bool:
        """
        Обновить полное имя пользователя.
        """
        user: Optional[User] = await self.get(tg_id)
        if not user:
            return False

        user.fullname = fullname
        await self.session.commit()
        return True
