"""
Операции с текстом администратора.
"""

from typing import Optional

from app.core.database.models import Admin

from .crud import AdminCRUD


class AdminText(AdminCRUD):
    """Менеджер для обновления текста администратора."""

    async def update_text(self, tg_id: int, new_text: str) -> bool:
        """
        Обновить текст администратора.
        """
        admin: Optional[Admin] = await self.get(tg_id)
        if not admin:
            return False

        admin.text = new_text
        await self.session.commit()
        return True
