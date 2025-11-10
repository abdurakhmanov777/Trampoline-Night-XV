"""
Базовый класс менеджера флагов.
"""

from sqlalchemy.ext.asyncio import AsyncSession


class FlagManagerBase:
    """Базовый класс для работы с таблицей Flag."""

    def __init__(
        self,
        session: AsyncSession
    ) -> None:
        """
        Инициализация менеджера флагов.

        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy.
        """
        self.session: AsyncSession = session
