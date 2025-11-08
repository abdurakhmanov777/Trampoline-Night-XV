"""
Основные настройки бота и приложения
"""

import os
from typing import List, Set

from dotenv import load_dotenv

load_dotenv()

# ------------------------------------------------------------
# Токен бота и база данных
# ------------------------------------------------------------
BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
DB_URL: str = os.getenv("DB_URL", "")

# ------------------------------------------------------------
# Настройки времени и администраторов
# ------------------------------------------------------------
TIME_ZONE: int = int(os.getenv("TIME_ZONE", "0"))
MAIN_ADMINS: List[int] = [
    int(x) for x in os.getenv("MAIN_ADMINS", "").split(",") if x
]

# ------------------------------------------------------------
# Символы и префиксы
# ------------------------------------------------------------
SYMB: str = os.getenv("SYMB", "")

# ------------------------------------------------------------
# Команды и callback-префиксы
# ------------------------------------------------------------
COMMAND_MAIN: Set[str] = {"start", "help", "test"}
CALLBACK_MAIN: Set[str] = {"start", "settings", "info", "miniapp"}
CALLBACK_SELECT: Set[str] = {"lang"}
