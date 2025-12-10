from typing import Any

import pymorphy3

# Создаем экземпляр морфологического анализатора
morph: pymorphy3.MorphAnalyzer = pymorphy3.MorphAnalyzer()

# Сопоставление падежей с кодами pymorphy3
CASES: dict[str, str] = {
    "именительный": "nomn",
    "родительный": "gent",
    "дательный": "datv",
    "винительный": "accs",
    "творительный": "ablt",
    "предложный": "loct"
}


async def inflect_text(
    text: str,
    case: str
) -> str:
    """
    Склоняет существительные и согласованные прилагательные
    в предложении в указанный падеж.

    Args:
        text: Исходная строка с одним или несколькими словами.
        case: Название падежа на русском языке.

    Returns:
        Строка с изменённым падежом или исходная строка,
        если подходящий падеж не найден.
    """
    case_code: str | None = CASES.get(case)
    if not case_code:
        return f"Неизвестный падеж: {case}"

    def choose_best_parse(word: str) -> Any:
        """
        Выбирает лучший разбор слова среди возможных.
        Предпочтение отдаётся существительным и прилагательным
        в именительном падеже.
        """
        parses: list[Any] = morph.parse(word)
        for p in parses:
            if "NOUN" in p.tag and "nomn" in p.tag:
                return p
            if "ADJF" in p.tag and "nomn" in p.tag:
                return p
        return parses[0]

    def preserve_case(original: str, new: str) -> str:
        """
        Сохраняет регистр букв исходного слова при склонении.
        """
        return "".join(
            n.upper() if o.isupper() else n.lower()
            for o, n in zip(original, new)
        ) + new[len(original):]

    words: list[str] = text.split()
    parsed: list[Any] = [choose_best_parse(w) for w in words]

    # Находим существительное для согласования
    noun: Any | None = next(
        (p for p in parsed if "NOUN" in p.tag),
        None
    )
    if not noun:
        return text

    number: str | None = noun.tag.number
    result: list[str] = []

    for word, parse in zip(words, parsed):
        # Склоняем существительное и согласованные прилагательные
        if parse == noun or (
                "ADJF" in parse.tag and parse.tag.number == number):
            tags: set[str] = set()

            # Особенности склонения винительного падежа
            if case_code == "accs":
                if "NOUN" in parse.tag:
                    if parse.tag.gender == "femn" and parse.tag.number == "sing":
                        tags.add("accs")
                    elif "anim" in parse.tag:
                        tags.add("accs")
                    else:
                        tags.add("nomn")
                elif "ADJF" in parse.tag:
                    if parse.tag.gender == "femn" and parse.tag.number == "sing":
                        tags.add("accs")
                    elif "anim" in noun.tag:
                        tags.add("accs")
                    else:
                        tags.add("nomn")
            else:
                tags.add(case_code)

            if number:
                tags.add(number)

            inflected: Any | None = parse.inflect(tags)
            new_word: str = inflected.word if inflected else word
            result.append(preserve_case(word, new_word))
        else:
            result.append(word)

    return " ".join(result)
