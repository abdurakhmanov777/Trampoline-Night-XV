import re

FIX_O_PATTERN = re.compile(r"\b([оО])\s+([«'“‘(]*)(\w)")
VOWELS = set('аеёиоуыэюяАЕЁИОУЫЭЮЯ')


async def fix_preposition_o(text: str) -> str:
    """
    Заменяет предлог о/О на об/Об перед словами, начинающимися на гласную букву.
    """
    def replacer(match):
        preposition, prefix, first_letter = match.groups()
        if first_letter in VOWELS:
            return f'{
                "Об" if preposition == "О" else "об"} {prefix}{first_letter}'
        return match.group(0)

    return FIX_O_PATTERN.sub(replacer, text)
