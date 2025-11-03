class DataTable:
    def __init__(self, id, name, row_count, db_id):
        self.id = id
        self.name = name
        self.row_count = row_count
        self.db_id = db_id

class Database:
    def __init__(self, id, name):
        self.id = id
        self.name = name

class TableDatabase:
    def __init__(self, db_id, table_id):
        self.db_id = db_id
        self.table_id = table_id

databases = [
    Database(1, 'производственная база данных'),
    Database(2, 'архивная база'),
    Database(3, 'тестовая база данных'),
    Database(4, 'другая производственная БД'),
    Database(5, 'архивная база (копия)'),
    Database(6, 'тестовая БД данных'),
]

tables = [
    DataTable(1, 'пользователи', 15000, 1),
    DataTable(2, 'заказы', 85000, 2),
    DataTable(3, 'продукты', 25000, 3),
    DataTable(4, 'покупатели', 35000, 3),
    DataTable(5, 'сотрудники', 5000, 3),
]

tables_databases = [
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

def main():
    one_to_many = [(t.name, t.row_count, d.name)
                   for d in databases
                   for t in tables
                   if t.db_id == d.id]

    many_to_many_temp = [(d.name, td.db_id, td.table_id)
                         for d in databases
                         for td in tables_databases
                         if d.id == td.db_id]

    many_to_many = [(t.name, t.row_count, db_name)
                    for db_name, db_id, table_id in many_to_many_temp
                    for t in tables if t.id == table_id]

    print('Запрос 1')
    print('Список всех связанных таблиц и баз данных, отсортированный по базам данных:')
    res1 = sorted(one_to_many, key=lambda i: i[2])
    for i in res1:
        print(i[2] + ": " + i[0] + ", строки: " + str(i[1]))

    print('\nЗапрос 2')
    print('Список баз данных с суммарным количеством строк таблиц в каждой БД:')
    res2_unsorted = []
    for d in databases:
        d_tables = list(filter(lambda i: i[2] == d.name, one_to_many))
        if len(d_tables) > 0:
            d_rows = [rows for _, rows, _ in d_tables]
            d_rows_sum = sum(d_rows)
            res2_unsorted.append((d.name, d_rows_sum))

    res2 = sorted(res2_unsorted, key=lambda i: i[1], reverse=True)
    for i in res2:
        print(i[0] + ": " + str(i[1]) + " строк")

    print('\nЗапрос 3')
    print('Список всех баз данных, у которых в названии присутствует слово "база", и список таблиц в них:')
    res3 = {}
    for d in databases:
        if 'база' in d.name.lower():
            d_tables = list(filter(lambda i: i[2] == d.name, many_to_many))
            d_tables_names = [x for x, _, _ in d_tables]
            res3[d.name] = d_tables_names

    for db_name, table_list in res3.items():
        print(db_name + ": " + " ,".join(table_list))

if __name__ == '__main__':
    main()
