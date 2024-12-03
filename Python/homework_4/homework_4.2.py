import itertools
import time

def infinite_number_generator(start=0):
    """Создание бесконечного генератора чисел."""
    for number in itertools.count(start):
        yield number

def apply_function_to_iterator(iterator, func):
    """Применение функции к каждому элементу в итераторе."""
    return (func(x) for x in iterator)

def combine_iterators(iterator1, iterator2):
    """Объединение нескольких итераторов в один."""
    return itertools.chain(iterator1, iterator2)

if __name__ == "__main__":
    try:
        # Задача 1: Создание бесконечного генератора чисел
        print("Бесконечный генератор чисел (первые 10 чисел):")
        for i, num in enumerate(infinite_number_generator()):
            if i >= 10:  # Ограничиваем вывод первыми 10 числами
                break
            print(num)

        # Задача 2: Применение функции к каждому элементу в итераторе
        square_func = lambda x: x ** 2
        print("\nКвадраты первых 5 чисел:")
        squares_iterator = apply_function_to_iterator(infinite_number_generator(), square_func)
        for i, square in enumerate(squares_iterator):
            if i >= 5:  # Ограничиваем вывод первыми 5 квадратами
                break
            print(square)

        # Задача 3: Объединение нескольких итераторов в один
        print("\nОбъединение двух итераторов:")
        iterator1 = itertools.count(1, 2)  # 1, 3, 5, 7, ...
        iterator2 = itertools.count(2, 3)  # 2, 5, 8, 11, ...
        combined_iterator = combine_iterators(iterator1, iterator2)
        for i, value in enumerate(combined_iterator):
            if i >= 10:  # Ограничиваем вывод первыми 10 значениями
                break
            print(value)

    except Exception as e:
        print(f"Произошла ошибка: {e}")