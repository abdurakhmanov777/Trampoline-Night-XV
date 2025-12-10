"""
Тест запуска и остановки Telegram-бота через терминал.

При запуске программы можно вводить:
    1 - запустить бота
    0 - остановить бота
    q - выйти из теста
"""

import asyncio

from loguru import logger

from app.config.settings import BOT_TOKEN
from app.core.bot.runner import run_bot, stop_bot


async def terminal_test() -> None:
    """Интерактивный тест запуска и остановки бота через терминал."""

    while True:
        cmd: str = await asyncio.to_thread(input)

        if cmd == "1":
            asyncio.create_task(run_bot(BOT_TOKEN))

        elif cmd == "0":
            stop_bot(BOT_TOKEN)

        elif cmd.lower() == "q":
            logger.info("Выход из теста")
            break


if __name__ == "__main__":
    try:
        asyncio.run(terminal_test())
    except (KeyboardInterrupt, asyncio.CancelledError):
        logger.warning("Тест прерван пользователем")
