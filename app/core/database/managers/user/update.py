"""
Обновление полей пользователя.

Содержит методы для изменения информации о пользователе
в таблице User.
"""

from typing import Optional

from app.core.database.models import User

from .crud import UserCRUD


class UserUpdate(UserCRUD):
    """Менеджер для обновления полей пользователя."""

    async def update_fullname(
        self,
        tg_id: int,
        fullname: str,
    ) -> bool:
        """
        Обновить полное имя пользователя.

        Args:
            tg_id (int): Telegram ID пользователя.
            fullname (str): Новое полное имя пользователя.

        Returns:
            bool: True, если обновление прошло успешно, иначе False.
        """
        user: Optional[User] = await self.get(tg_id)
        if not user:
            # Пользователь не найден
            return False

        user.fullname = fullname

        # Сохраняем изменения в базе данных
        await self.session.commit()
        return True
