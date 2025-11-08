"""
Настройки Google Sheets
"""

import os

from dotenv import load_dotenv

load_dotenv()

# ------------------------------------------------------------
# Настройки Google Sheets
# ------------------------------------------------------------
GSHEET_NAME: str = os.getenv("GSHEET_NAME", "Батутка XV Регистрации")
GSHEET_PAGE: str = os.getenv("GSHEET_PAGE", "Участники")
