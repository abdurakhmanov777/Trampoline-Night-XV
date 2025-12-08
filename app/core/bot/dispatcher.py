"""
Модуль для настройки диспетчера Telegram-бота и подключения роутеров
с соответствующими middleware.
"""

from typing import List, Tuple

from aiogram import Dispatcher, Router
from aiogram.dispatcher.event.telegram import TelegramEventObserver
from aiogram.fsm.storage.memory import MemoryStorage, SimpleEventIsolation

from app.core.bot import routers
from app.core.bot.middleware import MwBase, mw


async def setup_dispatcher() -> Dispatcher:
    """
    Асинхронная инициализация диспетчера и подключение роутеров с
    соответствующими middleware.

    Создает диспетчер с изоляцией событий в памяти, настраивает
    middleware для роутеров и подключает все роутеры к диспетчеру.

    Returns
    -------
    Dispatcher
        Экземпляр диспетчера с подключенными роутерами и middleware.
    """
    # Создаем диспетчер с изоляцией событий в памяти
    storage: MemoryStorage = MemoryStorage()
    dp: Dispatcher = Dispatcher(
        storage=storage,
        events_isolation=SimpleEventIsolation()
    )

    # Создание роутеров
    user_callback: Router = routers.get_router_user_callback()
    user_command: Router = routers.get_router_user_command()
    user_message: Router = routers.get_router_user_message()
    user_payment: Router = routers.get_router_user_payment()
    intercept_handler: Router = routers.get_router_intercept()

    # Настройка middleware
    middleware_map: List[Tuple[TelegramEventObserver, MwBase]] = [
        # Middleware для админов
        (routers.admin_callback.callback_query, mw.MwAdminCallback()),
        (routers.admin_command.message, mw.MwAdminMessage()),
        (routers.admin_message.message, mw.MwAdminMessage()),

        # Middleware для перехвата сообщений
        (intercept_handler.message, mw.MwIntercept()),

        # Middleware для пользователей
        (user_callback.callback_query, mw.MwUserCallback()),
        (user_command.message, mw.MwUserMessage()),
        (user_payment.callback_query, mw.MwUserCallback()),
        (user_payment.message, mw.MwUserPayment()),
        (user_message.message, mw.MwUserMessage()),
    ]

    for target, middleware in middleware_map:
        target.middleware(middleware)

    # Подключаем все роутеры к диспетчеру
    dp.include_routers(
        intercept_handler,
        user_callback,
        user_command,
        user_payment,
        user_message,
    )

    return dp
