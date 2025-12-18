import random

def gen_random(num_count, begin, end):
    for _ in range(num_count):
        yield random.randint(begin, end)


if __name__ == "__main__":
    print("Случайные числа:", list(gen_random(5, 1, 3)))
    print("Случайные числа:", list(gen_random(10, 0, 100)))
