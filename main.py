"""
Главная точка входа приложения.

Запускает Telegram-бота через app.core.runner.run_bot().
"""

import asyncio

from app.core.runner import run_bot

# Запуск бота
if __name__ == "__main__":
    # asyncio.run используется для выполнения асинхронной функции
    asyncio.run(run_bot())
