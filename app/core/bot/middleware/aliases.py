"""
Алиасы для создания middleware:

- MwCommand для command,
- MwMessage для message,
- MwCallback для callback_query.
"""

from typing import Any

from .base import MwBase


def MwAdminCallback(
    **extra_data: Any,
) -> MwBase:
    """
    Middleware для callback query админов.

    Args:
        **extra_data: дополнительные параметры для MwBase.

    Returns:
        MwBase: экземпляр middleware для админского callback.
    """
    return MwBase(
        delete_event=False,
        role="admin",
        **extra_data,
    )


def MwAdminCommand(
    **extra_data: Any,
) -> MwBase:
    """
    Middleware для команд админов с админской локализацией.

    Args:
        **extra_data: дополнительные параметры для MwBase.

    Returns:
        MwBase: экземпляр middleware для админской команды.
    """
    return MwBase(
        delete_event=True,
        role="admin",
        **extra_data,
    )


def MwAdminMessage(
    **extra_data: Any,
) -> MwBase:
    """
    Middleware для сообщений админов.

    Args:
        **extra_data: дополнительные параметры для MwBase.

    Returns:
        MwBase: экземпляр middleware для админского сообщения.
    """
    return MwBase(
        delete_event=True,
        role="admin",
        **extra_data,
    )


def MwSystemBlock(
    **extra_data: Any,
) -> MwBase:
    """
    Middleware для перехвата сообщений и callback'ов
    при активной системной блокировке бота.

    Args:
        **extra_data: дополнительные параметры для MwBase.

    Returns:
        MwBase: экземпляр middleware для системной блокировки.
    """
    return MwBase(
        delete_event=True,
        role="user",
        **extra_data,
    )


def MwUserCallback(
    **extra_data: Any,
) -> MwBase:
    """
    Middleware для callback query обычных пользователей.

    Args:
        **extra_data: дополнительные параметры для MwBase.

    Returns:
        MwBase: экземпляр middleware для пользовательского callback.
    """
    return MwBase(
        delete_event=False,
        role="user",
        **extra_data,
    )


def MwUserCommand(
    **extra_data: Any,
) -> MwBase:
    """
    Middleware для команд обычных пользователей.

    Args:
        **extra_data: дополнительные параметры для MwBase.

    Returns:
        MwBase: экземпляр middleware для пользовательской команды.
    """
    return MwBase(
        delete_event=True,
        role="user",
        **extra_data,
    )


def MwUserMessage(
    **extra_data: Any,
) -> MwBase:
    """
    Middleware для сообщений обычных пользователей.

    Args:
        **extra_data: дополнительные параметры для MwBase.

    Returns:
        MwBase: экземпляр middleware для пользовательского сообщения.
    """
    return MwBase(
        delete_event=True,
        role="user",
        **extra_data,
    )
