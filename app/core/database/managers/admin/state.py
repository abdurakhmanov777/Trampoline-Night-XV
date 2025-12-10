"""
Модуль управления стеком состояний администратора.

Содержит методы для добавления, удаления и просмотра
состояний администратора.
"""

from ...models import Admin
from .crud import AdminCRUD


class AdminState(AdminCRUD):
    """Менеджер состояний администратора."""

    async def push_state(
        self,
        tg_id: int,
        bot_id: int,
        new_state: str,
    ) -> bool:
        """
        Добавить новое состояние в стек администратора.

        Args:
            tg_id (int): Telegram ID администратора.
            bot_id (int): ID бота.
            new_state (str): Новое состояние для добавления.

        Returns:
            bool: True, если состояние добавлено, иначе False.
        """
        admin: Admin | None = await self.get(
            tg_id=tg_id,
            bot_id=bot_id
        )
        if not admin:
            # Администратор не найден
            return False

        stack: list[str] = admin.state.split(",") if admin.state else []
        stack.append(new_state)
        admin.state = ",".join(stack)

        # Сохраняем изменения в базе данных
        await self.session.commit()
        return True

    async def pop_state(
        self,
        tg_id: int,
        bot_id: int,
    ) -> str | None:
        """
        Удалить последнее состояние из стека администратора.

        Args:
            tg_id (int): Telegram ID администратора.
            bot_id (int): ID бота.

        Returns:
            str | None: Удалённое состояние или None, если
                стек пуст или администратор не найден.
        """
        admin: Admin | None = await self.get(
            tg_id=tg_id,
            bot_id=bot_id,
        )
        if not admin:
            return None

        stack: list[str] = admin.state.split(",") if admin.state else []
        if not stack:
            # Стек пуст
            return None

        last_state: str = stack.pop()
        admin.state = ",".join(stack)
        await self.session.commit()
        return last_state

    async def peek_state(
        self,
        tg_id: int,
        bot_id: int,
    ) -> str | None:
        """
        Получить текущее состояние без удаления.

        Args:
            tg_id (int): Telegram ID администратора.
            bot_id (int): ID бота.

        Returns:
            str | None: Последнее состояние в стеке или None,
                если стек пуст или администратор не найден.
        """
        admin: Admin | None = await self.get(
            tg_id=tg_id,
            bot_id=bot_id,
        )
        if not admin:
            return None

        stack: list[str] = admin.state.split(",") if admin.state else []
        return stack[-1] if stack else None
