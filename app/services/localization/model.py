from typing import Optional


class Localization:
    """
    Класс для хранения и доступа к данным локализации.

    Позволяет обращаться к переведённым строкам через атрибуты,
    автоматически создавая вложенные объекты для словарей.
    """

    default: Optional['Localization']

    def __init__(
        self,
        localization_data: dict
    ) -> None:
        """
        Инициализирует объект локализации на основе словаря.

        Args:
            localization_data (dict): Данные локализации в виде словаря.
        """
        self._parse_data(localization_data)

    def _parse_data(
        self,
        data: dict
    ) -> None:
        """
        Рекурсивно создаёт атрибуты для ключей словаря локализации.

        Если значение является словарём, создаётся вложенный объект
        Localization. Иначе значение сохраняется как обычный атрибут.
        """
        for key, value in data.items():
            # Если значение — словарь, создаём вложенный объект
            if isinstance(value, dict):
                setattr(self, key, Localization(value))
            else:
                setattr(self, key, value)
