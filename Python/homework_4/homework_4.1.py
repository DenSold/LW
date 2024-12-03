from datetime import datetime, timedelta

def display_current_datetime():
    # Отображение текущей даты и времени
    current_datetime = datetime.now()
    print("Текущая дата и время:", current_datetime)

def calculate_date_difference(date1, date2):
    # Вычисление разницы между двумя датами
    difference = date2 - date1
    print(f"Разница между {date2.date()} и {date1.date()} составляет {difference.days} дней.")

def convert_string_to_datetime(date_string, date_format):
    # Преобразование строки в объект даты и времени
    converted_date = datetime.strptime(date_string, date_format)
    print("Преобразованная дата и время:", converted_date)
    return converted_date

if __name__ == "__main__":
    # Задача 1: Отображение текущей даты и времени
    display_current_datetime()

    # Задача 2: Вычисление разницы между двумя датами
    date1 = datetime(2023, 1, 1)  # Первая дата
    date2 = datetime(2024, 1, 5)  # Вторая дата
    calculate_date_difference(date1, date2)

    # Задача 3: Преобразование строки в объект даты и времени
    date_string = "2024-05-09 21:00:00"
    date_format = "%Y-%m-%d %H:%M:%S"
    converted_date = convert_string_to_datetime(date_string, date_format)