"""
Операции с текстом администратора.

Содержит методы для обновления текста администратора
в базе данных.
"""

from typing import Optional

from ...models import Admin
from .crud import AdminCRUD


class AdminText(AdminCRUD):
    """Менеджер для обновления текста администратора."""

    async def update_text(
        self,
        tg_id: int,
        chat_id: int,
        new_text: str,
    ) -> bool:
        """
        Обновить текст администратора.

        Args:
            tg_id (int): Telegram ID администратора.
            chat_id (int): ID бота.
            new_text (str): Новый текст администратора.

        Returns:
            bool: True, если текст успешно обновлён, иначе False.
        """
        admin: Optional[Admin] = await self.get(
            tg_id=tg_id,
            chat_id=chat_id,)
        if not admin:
            # Администратор не найден
            return False

        admin.text = new_text

        # Сохраняем изменения в базе данных
        await self.session.commit()
        return True
