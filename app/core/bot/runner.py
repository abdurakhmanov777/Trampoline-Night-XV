"""
Модуль для запуска и остановки Telegram-ботов и проверки их состояния.

Содержит функции для управления жизненным циклом ботов через PollingManager,
включая регистрацию команд и настройку диспетчера.
"""

import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types.user import User
from loguru import logger

from .commands import register_bot_commands
from .dispatcher import setup_dispatcher
from .services.polling import PollingManager, get_polling_manager


async def run_bot(
    api_tokens: str | list[str],
) -> bool:
    """Запускает одного или нескольких Telegram-ботов.

    Args:
        api_tokens (str | list[str]): API-токен бота или список токенов.

    Returns:
        bool: True, если хотя бы один бот успешно запущен, иначе False.
    """
    if isinstance(api_tokens, str):
        api_tokens = [api_tokens]

    dispatcher: Dispatcher = await setup_dispatcher()
    polling_manager: PollingManager = get_polling_manager()

    async def start_single_bot(token: str) -> bool:
        """Запускает одного бота по API-токену.

        Args:
            token (str): API-токен бота.

        Returns:
            bool: True, если бот успешно запущен, иначе False.
        """
        if polling_manager.is_bot_running(token):
            logger.warning("Бот запущен, повторный запуск отклонен")
            return False

        try:
            async with Bot(token) as bot:
                await register_bot_commands(bot)

                async def on_startup() -> None:
                    """Обрабатывает запуск бота."""
                    bot_info: User = await bot.get_me()
                    logger.debug(f"Бот @{bot_info.username} запущен")

                async def on_shutdown() -> None:
                    """Обрабатывает остановку бота."""
                    logger.debug(f"Бот остановлен")

                polling_manager.start_bot_polling(
                    dp=dispatcher,
                    api_token=token,
                    on_bot_startup=on_startup,
                    on_bot_shutdown=on_shutdown,
                )

                # Ждем, пока бот не будет остановлен
                while polling_manager.is_bot_running(token):
                    await asyncio.sleep(1)

            return True

        except Exception as error:
            logger.exception(f"Ошибка при запуске бота {token}: {error}")
            return False

    results: list[bool] = await asyncio.gather(
        *(start_single_bot(t) for t in api_tokens)
    )
    return any(results)


def stop_bot(
    api_tokens: str | list[str],
) -> bool:
    """Останавливает одного или нескольких Telegram-ботов.

    Args:
        api_tokens (str | list[str]): API-токен бота или список токенов.

    Returns:
        bool: True, если хотя бы один бот был остановлен, иначе False.
    """
    if isinstance(api_tokens, str):
        api_tokens = [api_tokens]

    polling_manager: PollingManager = get_polling_manager()
    stopped_any: bool = False

    for token in api_tokens:
        try:
            if not polling_manager.is_bot_running(token):
                logger.warning(f"Бот не запущен, остановка отклонена")
                continue

            polling_manager.stop_bot_polling(token)
            stopped_any = True

        except Exception as error:
            logger.exception(f"Ошибка при остановке бота {token}: {error}")

    return stopped_any
