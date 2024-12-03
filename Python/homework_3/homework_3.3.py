import requests
from bs4 import BeautifulSoup

# URL для получения данных
url = 'https://vk.com'

# Получение данных с веб-сайта
response = requests.get(url)

# Проверка успешности запроса
if response.status_code == 200:
    # Парсинг HTML-кода
    soup = BeautifulSoup(response.content, 'html.parser')

    # Пример: получение заголовка страницы
    title = soup.title.string
    print(f"Заголовок страницы: {title}")

    # Пример: получение всех ссылок на странице
    links = soup.find_all('a')
    print("Все ссылки на странице:")
    for link in links:
        print(link.get('href'))
else:
    print(f"Ошибка при получении данных: {response.status_code}")