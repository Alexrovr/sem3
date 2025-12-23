def field(items, *args):
    """
    Генератор для выборки полей из списка словарей.

    Args:
        items: Список словарей
        *args: Поля для выборки (одно или несколько)

    Yields:
        Значение поля (если передан один аргумент)
        или словарь с выбранными полями (если передано несколько аргументов)

    Raises:
        AssertionError: если не передано ни одного поля для выборки
    """
    assert len(args) > 0, "Должен быть указан хотя бы один аргумент"

    if len(args) == 1:
        key = args[0]
        for item in items:
            if key in item and item[key] is not None:
                yield item[key]
    else:
        for item in items:
            result = {}
            for key in args:
                if key in item and item[key] is not None:
                    result[key] = item[key]
            if result:
                yield result


class GoodsManager:
    """Класс для управления товарами с использованием функции field"""

    def __init__(self, goods=None):
        self.goods = goods or []

    def get_titles(self):
        """Получить все названия товаров"""
        return list(field(self.goods, 'title'))

    def get_titles_and_prices(self):
        """Получить названия и цены товаров"""
        return list(field(self.goods, 'title', 'price'))

    def get_prices_by_color(self, color):
        """Получить цены товаров определенного цвета (с использованием mock)"""
        filtered_goods = [item for item in self.goods if item.get('color') == color]
        return list(field(filtered_goods, 'price'))


def main():
    """Пример использования функции field"""
    goods = [
        {'title': 'Ковер', 'price': 2000, 'color': 'green'},
        {'title': 'Диван для отдыха', 'color': 'black'},
        {'title': None, 'price': 3000, 'color': 'blue'},
        {'title': 'Стул', 'price': None, 'color': 'red'}
    ]

    print("Тест 1 (один аргумент):")
    for title in field(goods, 'title'):
        print(title)

    print("\nТест 2 (несколько аргументов):")
    for item in field(goods, 'title', 'price'):
        print(item)


if __name__ == "__main__":
    main()
