class DataBuffer:
    def __init__(self):
        self.buffer = []

    def add_data(self, data):
        """Добавляет данные в буфер. Если буфер переполнен (>=5 элементов), выводит сообщение и очищает его."""
        self.buffer.append(data)
        if len(self.buffer) >= 5:
            print("Буфер переполнен. Очистка буфера.")
            self.buffer.clear()

    def get_data(self):
        """Возвращает данные из буфера. Если буфер пуст, выводит сообщение об отсутствии данных."""
        if not self.buffer:
            print("Буфер пуст. Нет данных для получения.")
            return None
        return self.buffer

buffer = DataBuffer()

buffer.add_data(1)
buffer.add_data(2)
buffer.add_data(3)
buffer.add_data(4)
buffer.add_data(5)  # Это добавление вызовет переполнение и очистку буфера

print(buffer.get_data())  # Буфер пуст, так как он был очищен

buffer.add_data(10)
print(buffer.get_data())