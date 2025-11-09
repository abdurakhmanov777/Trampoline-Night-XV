import re
from typing import Any, Match

# Шаблон для поиска предлога "о" перед словами
FIX_O_PATTERN: re.Pattern = re.compile(
    r"\b([оО])\s+([«'“‘(]*)(\w)"
)

# Множество гласных букв русского алфавита
VOWELS: set[str] = set("аеёиоуыэюяАЕЁИОУЫЭЮЯ")


async def fix_preposition_o(
        text: str
) -> str:
    """
    Исправляет предлог 'о' на 'об' перед словами, начинающимися
    с гласной буквы.

    Args:
        text: Исходный текст.

    Returns:
        Текст с исправленным предлогом 'о' на 'об' перед гласной.
    """
    def replacer(match: Match[str]) -> str:
        """
        Заменяет предлог в найденном совпадении.

        Args:
            match: Объект регулярного выражения с совпадением.

        Returns:
            Исправленный предлог с остальной частью слова.
        """
        preposition: str | Any
        prefix: str | Any
        first_letter: str | Any
        preposition, prefix, first_letter = match.groups()
        
        if first_letter in VOWELS:
            corrected: str = (
                "Об" if preposition == "О" else "об"
            ) + f" {prefix}{first_letter}"
            return corrected
        return match.group(0)

    # Заменяем все случаи предлога "о" перед гласными
    return FIX_O_PATTERN.sub(replacer, text)
