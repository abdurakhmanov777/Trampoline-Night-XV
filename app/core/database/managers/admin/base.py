"""
Базовый класс менеджера администраторов.
"""

from sqlalchemy.ext.asyncio import AsyncSession


class AdminManagerBase:
    """Базовый менеджер администраторов."""

    def __init__(self, session: AsyncSession) -> None:
        """
        Инициализация менеджера.

        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy.
        """
        self.session: AsyncSession = session
