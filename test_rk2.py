# test_refactored_code.py
import unittest

# Импортируем функции из рефакторированного кода
from rk2 import (
    DataTable, Database, TableDatabase,
    initialize_data, build_one_to_many, build_many_to_many,
    query1_sorted_tables, query2_databases_with_row_sum,
    query3_databases_with_base_in_name
)

class TestDatabaseQueries(unittest.TestCase):

    def setUp(self):
        """Подготовка тестовых данных перед каждым тестом"""
        self.databases = [
            Database(1, 'производственная база данных'),
            Database(2, 'архивная база'),
            Database(3, 'тестовая база данных'),
            Database(4, 'другая производственная БД'),
            Database(5, 'архивная база (копия)'),
            Database(6, 'тестовая БД данных'),
        ]

        self.tables = [
            DataTable(1, 'пользователи', 15000, 1),
            DataTable(2, 'заказы', 85000, 2),
            DataTable(3, 'продукты', 25000, 3),
            DataTable(4, 'покупатели', 35000, 3),
            DataTable(5, 'сотрудники', 5000, 3),
        ]

        self.tables_databases = [
            TableDatabase(1, 1),
            TableDatabase(2, 2),
            TableDatabase(3, 3),
            TableDatabase(3, 4),
            TableDatabase(3, 5),
            TableDatabase(4, 1),
            TableDatabase(5, 2),
            TableDatabase(6, 3),
            TableDatabase(6, 4),
            TableDatabase(6, 5),
        ]

    def test_build_one_to_many(self):
        """Тест 1: Проверка построения отношения один-ко-многим"""
        result = build_one_to_many(self.databases, self.tables)

        # Проверяем количество связей
        self.assertEqual(len(result), 5)

        # Проверяем, что каждая связь содержит имя таблицы, количество строк и имя БД
        for table_name, row_count, db_name in result:
            self.assertIsInstance(table_name, str)
            self.assertIsInstance(row_count, int)
            self.assertIsInstance(db_name, str)

        # Проверяем конкретные связи
        db_names = [db_name for _, _, db_name in result]
        self.assertIn('производственная база данных', db_names)
        self.assertIn('архивная база', db_names)
        self.assertIn('тестовая база данных', db_names)

    def test_query1_sorted_tables(self):
        """Тест 2: Проверка запроса 1 - сортировка таблиц по именам баз данных"""
        result = query1_sorted_tables(self.databases, self.tables)

        # Проверяем, что результат отсортирован по именам БД
        db_names = [db_name for _, _, db_name in result]
        sorted_db_names = sorted(db_names)
        self.assertEqual(db_names, sorted_db_names)

        # Проверяем, что все элементы присутствуют
        self.assertEqual(len(result), 5)

        # Проверяем первый элемент (должен быть 'архивная база')
        self.assertEqual(result[0][2], 'архивная база')

    def test_query3_databases_with_base_in_name(self):
        """Тест 3: Проверка запроса 3 - поиск БД с 'база' в названии"""
        result = query3_databases_with_base_in_name(
            self.databases, self.tables, self.tables_databases
        )

        # Проверяем тип результата
        self.assertIsInstance(result, dict)

        # Проверяем, что в результате только БД с 'база' в названии
        for db_name in result.keys():
            self.assertIn('база', db_name.lower())

        # Проверяем конкретные БД
        expected_dbs = ['архивная база', 'архивная база (копия)',
                       'производственная база данных', 'тестовая база данных']

        for db_name in expected_dbs:
            self.assertIn(db_name, result)

        # Проверяем, что БД без 'база' в названии не попали в результат
        self.assertNotIn('другая производственная БД', result)
        self.assertNotIn('тестовая БД данных', result)

        # Проверяем, что у каждой БД есть список таблиц
        for db_name, tables_list in result.items():
            self.assertIsInstance(tables_list, list)

    def test_initialize_data_function(self):
        """Дополнительный тест: Проверка функции инициализации данных"""
        databases, tables, tables_databases = initialize_data()

        # Проверяем количество элементов
        self.assertEqual(len(databases), 6)
        self.assertEqual(len(tables), 5)
        self.assertEqual(len(tables_databases), 10)

        # Проверяем типы объектов
        self.assertIsInstance(databases[0], Database)
        self.assertIsInstance(tables[0], DataTable)
        self.assertIsInstance(tables_databases[0], TableDatabase)

if __name__ == '__main__':
    unittest.main(verbosity=2)
