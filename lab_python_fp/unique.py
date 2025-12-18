class Unique(object):
    def __init__(self, items, **kwargs):
        self.items = iter(items)
        self.ignore_case = kwargs.get('ignore_case', False)
        self.seen = set()

    def __next__(self):
        while True:
            try:
                item = next(self.items)
                key = item.lower() if (self.ignore_case and isinstance(item, str)) else item

                if key not in self.seen:
                    self.seen.add(key)
                    return item
            except StopIteration:
                raise StopIteration

    def __iter__(self):
        return self


if __name__ == "__main__":
    data1 = [1, 1, 1, 1, 1, 2, 2, 2, 2, 2]
    print("Тест 1 (числа):", list(Unique(data1)))

    from gen_random import gen_random
    data2 = gen_random(10, 1, 3)
    print("Тест 2 (генератор):", list(Unique(data2)))

    data3 = ['a', 'A', 'b', 'B', 'a', 'A', 'b', 'B']
    print("Тест 3 (без ignore_case):", list(Unique(data3)))
    print("Тест 4 (с ignore_case):", list(Unique(data3, ignore_case=True)))
