"""
Модуль управления стеком состояний администратора.
"""

from typing import List, Optional

from app.core.database.models import Admin

from .crud import AdminCRUD


class AdminState(AdminCRUD):
    """Менеджер состояний администратора."""

    async def push_state(self, tg_id: int, new_state: str) -> bool:
        """
        Добавить новое состояние в стек администратора.
        """
        admin: Optional[Admin] = await self.get(tg_id)
        if not admin:
            return False

        stack: List[str] = admin.state.split(",") if admin.state else []
        stack.append(new_state)
        admin.state = ",".join(stack)
        await self.session.commit()
        return True

    async def pop_state(self, tg_id: int) -> Optional[str]:
        """
        Удалить последнее состояние из стека администратора.
        """
        admin: Optional[Admin] = await self.get(tg_id)
        if not admin:
            return None

        stack: List[str] = admin.state.split(",") if admin.state else []
        if not stack:
            return None

        last_state: str = stack.pop()
        admin.state = ",".join(stack)
        await self.session.commit()
        return last_state

    async def peek_state(self, tg_id: int) -> Optional[str]:
        """
        Получить текущее состояние без удаления.
        """
        admin: Optional[Admin] = await self.get(tg_id)
        if not admin:
            return None

        stack: List[str] = admin.state.split(",") if admin.state else []
        return stack[-1] if stack else None
