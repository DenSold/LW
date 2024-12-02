def read_numeric_lines(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = file.readlines()

        for line in data:
            line = line.strip()  # Убираем символы новой строки и пробелы по краям
            if line.isdigit() or (
                    line.replace('.', '', 1).isdigit() and line.count('.') < 2):  # Проверка, что строка является числом
                print(line)
            else:
                raise TypeError(f"Некорректное значение в файле: '{line}' не является числом")

    except FileNotFoundError:
        print(f"Файл '{filename}' не найден.")
    except TypeError as e:
        print(e)


# Пример использования
read_numeric_lines('check.txt')