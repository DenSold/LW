from collections import Counter
import re

def count_unique_words(text):
    # Убираем знаки препинания и приводим текст к нижнему регистру
    cleaned_text = re.sub(r'[^\w\s]', '', text).lower()
    # Разделяем строку на слова
    words = cleaned_text.split()
    # Используем Counter для подсчета уникальных слов
    word_count = Counter(words)
    # Возвращаем количество уникальных слов
    return len(word_count)

# Пример использования
text = "Ура! Как хорошо! Ура!"
unique_words_count = count_unique_words(text)
print(f"Количество уникальных слов: {unique_words_count}")