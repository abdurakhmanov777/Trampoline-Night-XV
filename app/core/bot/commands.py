"""
Модуль для регистрации команд Telegram-бота в приватных чатах.

Добавляет команды, доступные в личных сообщениях. Для администраторов
дополнительно устанавливается команда /admin.
"""

from typing import Sequence

from aiogram import Bot, types
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import BotCommandScopeAllPrivateChats, BotCommandScopeChat
from loguru import logger

from app.config.settings import MAIN_ADMINS


async def register_bot_commands(
    bot: Bot,
) -> None:
    """Регистрирует команды Telegram-бота.

    Команды для всех пользователей регистрируются только в приватных чатах.
    Для администраторов устанавливается расширенный набор команд.

    Args:
        bot (Bot): Экземпляр Telegram-бота.

    Returns:
        None: Функция не возвращает значения.
    """
    user_commands: Sequence[types.BotCommand] = [
        types.BotCommand(
            command="start",
            description="Запуск или перезапуск бота",
        ),
        types.BotCommand(
            command="cancel",
            description="Отмена регистрации",
        ),
        types.BotCommand(
            command="help",
            description="Техническая поддержка",
        ),
        types.BotCommand(
            command="id",
            description="Узнать ID чата",
        ),
    ]

    # Регистрация команд, доступных всем пользователям
    await bot.set_my_commands(
        commands=user_commands,
        scope=BotCommandScopeAllPrivateChats(),
    )

    admin_commands: Sequence[types.BotCommand] = [
        *user_commands,
        types.BotCommand(
            command="admin",
            description="Админ-панель",
        ),
    ]

    # Попытка зарегистрировать расширенные команды для администраторов
    for admin_id in MAIN_ADMINS:
        try:
            await bot.set_my_commands(
                commands=admin_commands,
                scope=BotCommandScopeChat(
                    chat_id=admin_id,
                ),
            )
        except TelegramBadRequest:
            # Логируем, если чат администратора ещё не существует
            logger.warning(
                f"Невозможно установить команды для admin_id={admin_id}: "
                "чат не найден"
            )
