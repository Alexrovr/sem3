import unittest
from unittest.mock import Mock, patch, MagicMock
from field_module import GoodsManager, field


class TestFieldWithMocks(unittest.TestCase):
    """Тесты с использованием Mock-объектов"""

    def test_field_with_mock_iterator(self):
        """Тест с mock-итератором"""
        # Создаем mock-объект, который ведет себя как итератор
        mock_items = Mock()
        mock_items.__iter__ = Mock(return_value=iter([
            {'title': 'Mock1', 'price': 100},
            {'title': 'Mock2', 'price': 200}
        ]))

        result = list(field(mock_items, 'title'))
        self.assertEqual(result, ['Mock1', 'Mock2'])

    def test_goods_manager_with_mock_data(self):
        """Тест GoodsManager с mock-данными"""
        # Создаем mock-список товаров
        mock_goods = [
            {'title': 'Mock Chair', 'price': 1500},
            {'title': 'Mock Table', 'price': 2500}
        ]

        manager = GoodsManager(mock_goods)
        titles = manager.get_titles()
        self.assertEqual(titles, ['Mock Chair', 'Mock Table'])

    @patch('field_module.field')
    def test_get_titles_with_mocked_field(self, mock_field):
        """Тест с мокированием самой функции field"""
        # Настраиваем mock
        mock_field.return_value = ['Mocked Title 1', 'Mocked Title 2']

        manager = GoodsManager([{'title': 'Test'}])
        result = manager.get_titles()

        # Проверяем, что field была вызвана с правильными аргументами
        mock_field.assert_called_once_with([{'title': 'Test'}], 'title')
        self.assertEqual(result, ['Mocked Title 1', 'Mocked Title 2'])

    def test_get_prices_by_color_with_mock(self):
        """Тест фильтрации по цвету с использованием mock"""
        # Создаем mock-объект для списка товаров
        mock_goods = MagicMock()

        # Настраиваем поведение фильтрации
        def filter_side_effect(func):
            filtered = [
                {'price': 2000, 'color': 'green'},
                {'price': 1500, 'color': 'green'}
            ]
            return [item for item in filtered if func(item)]

        mock_goods.__iter__ = Mock()
        mock_goods.__iter__.return_value = [
            {'price': 2000, 'color': 'green'},
            {'price': 1500, 'color': 'green'},
            {'price': 3000, 'color': 'blue'}
        ]

        manager = GoodsManager(mock_goods.__iter__.return_value)
        prices = manager.get_prices_by_color('green')

        self.assertEqual(prices, [2000, 1500])


class TestFieldIntegration(unittest.TestCase):
    """Интеграционные тесты с комбинацией реальных и mock-объектов"""

    def test_integration_with_mock_database(self):
        """Интеграционный тест с mock-базой данных"""
        # Создаем mock для "базы данных"
        class MockDatabase:
            def get_goods(self):
                return [
                    {'title': 'DB Item 1', 'price': 1000},
                    {'title': 'DB Item 2', 'price': 2000}
                ]

        mock_db = MockDatabase()

        # Используем реальную функцию field с данными из mock-базы
        goods = mock_db.get_goods()
        result = list(field(goods, 'title', 'price'))

        expected = [
            {'title': 'DB Item 1', 'price': 1000},
            {'title': 'DB Item 2', 'price': 2000}
        ]
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main(verbosity=2)
