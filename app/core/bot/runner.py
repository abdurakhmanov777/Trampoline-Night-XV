"""
Модуль запуска Telegram-бота.
"""

from aiogram import Bot, Dispatcher
from aiogram.types.user import User
from loguru import logger

from .commands import register_bot_commands
from .dispatcher import setup_dispatcher
from .factory import create_bot


async def run_bot() -> None:
    """
    Инициализация и запуск Telegram-бота.

    Последовательность действий:
        1. Создание экземпляра бота.
        2. Регистрация команд бота.
        3. Настройка диспетчера.
        4. Запуск polling с колбэком on_startup.
        5. Корректное завершение сессии бота.
    """
    # Создание бота и получение информации о нём
    bot: Bot = await create_bot()
    bot_info: User = await bot.get_me()
    logger.debug(f"Бот @{bot_info.username} создан")

    # Регистрация команд
    await register_bot_commands(bot)
    logger.debug("Команды бота зарегистрированы")

    # Настройка диспетчера
    dp: Dispatcher = await setup_dispatcher()
    logger.debug("Диспетчер настроен")

    async def on_startup(
        bot: Bot
    ) -> None:
        """
        Callback при запуске polling.
        """
        logger.debug("Polling бота запущен")

    dp.startup.register(on_startup)

    # Запуск polling
    await dp.start_polling(bot)

    # Закрытие сессии бота после завершения
    await bot.session.close()
