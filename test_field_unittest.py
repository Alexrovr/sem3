import unittest
from field_module import field, GoodsManager


class TestFieldFunction(unittest.TestCase):
    """Тесты для функции field с использованием unittest"""

    def setUp(self):
        """Подготовка тестовых данных"""
        self.goods = [
            {'title': 'Ковер', 'price': 2000, 'color': 'green'},
            {'title': 'Диван для отдыха', 'color': 'black'},
            {'title': None, 'price': 3000, 'color': 'blue'},
            {'title': 'Стул', 'price': None, 'color': 'red'}
        ]

    def test_single_field(self):
        """Тест 1: выборка одного поля"""
        result = list(field(self.goods, 'title'))
        expected = ['Ковер', 'Диван для отдыха', 'Стул']
        self.assertEqual(result, expected)

    def test_multiple_fields(self):
        """Тест 2: выборка нескольких полей"""
        result = list(field(self.goods, 'title', 'price'))
        expected = [
            {'title': 'Ковер', 'price': 2000},
            {'title': 'Диван для отдыха'},
            {'price': 3000},
            {'title': 'Стул'}
        ]
        self.assertEqual(result, expected)

    def test_none_values_filtered(self):
        """Тест 3: значения None должны фильтроваться"""
        result = list(field(self.goods, 'price'))
        expected = [2000, 3000]
        self.assertEqual(result, expected)

    def test_no_args_exception(self):
        """Тест 4: проверка вызова исключения без аргументов"""
        with self.assertRaises(AssertionError):
            list(field(self.goods))

    def test_empty_list(self):
        """Тест 5: обработка пустого списка"""
        result = list(field([], 'title'))
        self.assertEqual(result, [])


class TestGoodsManager(unittest.TestCase):
    """Тесты для класса GoodsManager"""

    def test_get_titles(self):
        """Тест получения названий товаров"""
        goods = [
            {'title': 'Ковер', 'price': 2000},
            {'title': 'Диван', 'price': 5000}
        ]
        manager = GoodsManager(goods)
        titles = manager.get_titles()
        self.assertEqual(titles, ['Ковер', 'Диван'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
