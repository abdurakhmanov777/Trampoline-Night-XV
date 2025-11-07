"""
Настройки Google Sheets
"""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# ------------------------------------------------------------
# Настройки Google Sheets
# ------------------------------------------------------------
GSHEET_NAME: str = os.getenv("NAME_GOOGLESHEETS", "Батутка XV Регистрации")
GSHEET_TAB: str = os.getenv("GOOGLE_SHEET_WORKSHEET", "Участники")
GSHEET_CREDS: Path = Path("credentials/creds.json")
