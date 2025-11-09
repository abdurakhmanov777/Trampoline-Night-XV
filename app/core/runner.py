"""
Главная функция запуска Telegram-бота.
"""

import asyncio

from aiogram import Bot, Dispatcher
from loguru import logger

from .commands import register_bot_commands
from .database import async_main
from .dispatcher import setup_dispatcher
from .factory import create_bot
from .logging_config import configure_logging


async def run_bot() -> None:
    """
    Запускает Telegram-бота.

    Включает:
      - Настройку логирования
      - Инициализацию базы данных
      - Создание бота
      - Регистрацию команд
      - Инициализацию диспетчера и роутеров
      - Запуск polling
    """
    configure_logging()
    bot: Bot | None = None

    try:
        # Инициализация базы данных
        await async_main()

        # Создание экземпляра бота
        bot = await create_bot()
        await register_bot_commands(bot)

        # Настройка диспетчера
        dp: Dispatcher = await setup_dispatcher()

        logger.debug("Бот включен, запускаем polling")
        await dp.start_polling(bot, dp_for_new_bot=dp)

    except (KeyboardInterrupt, asyncio.CancelledError):
        logger.debug("Завершение работы по сигналу отмены или Ctrl+C")

    except Exception as e:
        logger.exception(f"Необработанная ошибка: {e}")

    finally:
        if bot:
            await bot.session.close()
        logger.debug("Бот отключен")
