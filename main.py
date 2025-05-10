from urllib.parse import urlsplit, unquote
import os.path
import requests
import os
import concurrent.futures

def get_file_from_wiki():
    filename = "HST-SM4.jpeg"
    url = "https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg"

    headers = {
        "User-Agent": "MyPythonApp/1.0 (https://example.com/contact)"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        with open(filename, 'wb') as file:
            file.write(response.content)
        print(f"Файл {filename} успешно сохранён.")
    except requests.RequestException as e:
        print(f"Ошибка загрузки файла: {e}")

def get_file_extension(url: str) -> str:
    path = urlsplit(url).path
    path = unquote(path)
    filename = os.path.split(path)[1]
    _, ext = os.path.splitext(filename)
    return ext


def fetch_spacex_last_launch():
    os.makedirs("images", exist_ok=True)
    url = "https://api.spacexdata.com/v5/launches"
    response = requests.get(url)
    response.raise_for_status()
    launches = response.json()

    for launch in launches[::-1]:
        photos = launch.get("links", {}).get("flickr", {}).get("original", [])
        if photos:
            print(f"Название запуска: {launch.get('name')}")
            print("Ссылки на фото:")
            for photo_url in photos:
                print(photo_url)

            def download(photo_url, i):
                try:
                    img_data = requests.get(photo_url).content
                    filename = os.path.join("images", f"spacex_photo_{i + 1}.jpg")
                    with open(filename, 'wb') as f:
                        f.write(img_data)
                except Exception as e:
                    print(f"Не удалось загрузить {photo_url}: {e}")

            with concurrent.futures.ThreadPoolExecutor() as executor:
                for i, photo_url in enumerate(photos):
                    executor.submit(download, photo_url, i)
            break
    else:
        print("Фото не найдены ни в одном из последних запусков.")


fetch_spacex_last_launch()


# Функция для загрузки изображений NASA APOD
def fetch_nasa_apod_images(api_key: str, count: int = 30):
    os.makedirs("nasa_images", exist_ok=True)
    url = "https://api.nasa.gov/planetary/apod"
    params = {"api_key": api_key, "count": count}

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Ошибка запроса к NASA API: {e}")
        return

    items = response.json()

    def download(item, i):
        if item.get("media_type") != "image":
            return
        img_url = item.get("url")
        if not img_url:
            return
        ext = get_file_extension(img_url) or ".jpg"
        filename = os.path.join("nasa_images", f"nasa_apod_{i + 1}{ext}")
        try:
            img_data = requests.get(img_url).content
            with open(filename, 'wb') as f:
                f.write(img_data)
        except Exception as e:
            print(f"Не удалось загрузить {img_url}: {e}")

    with concurrent.futures.ThreadPoolExecutor() as executor:
        for i, item in enumerate(items):
            executor.submit(download, item, i)

def get_nasa_epic_image_url(api_key: str):
    url = "https://api.nasa.gov/EPIC/api/natural/images"
    params = {"api_key": api_key}

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Ошибка запроса к NASA EPIC API: {e}")
        return

    items = response.json()
    if not items:
        print("Нет данных EPIC.")
        return

    # Берем первое изображение
    image_info = items[0]
    image_name = image_info['image']
    date_str = image_info['date']  # формат "2024-05-08 00:11:29"

    # Разбиваем дату
    date_parts = date_str.split()[0].split('-')  # ['2024', '05', '08']
    year, month, day = date_parts

    image_url = f"https://api.nasa.gov/EPIC/archive/natural/{year}/{month}/{day}/png/{image_name}.png?api_key={api_key}"
    print("Ссылка на фото Земли (EPIC):", image_url)

def fetch_nasa_epic_images(api_key: str, count: int = 10):
    os.makedirs("epic_images", exist_ok=True)
    url = "https://api.nasa.gov/EPIC/api/natural/images"
    params = {"api_key": api_key}

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Ошибка запроса к NASA EPIC API: {e}")
        return

    items = response.json()
    if not items:
        print("Нет данных EPIC.")
        return

    def download(item, i):
        image_name = item['image']
        date_str = item['date']
        year, month, day = date_str.split()[0].split('-')
        image_url = f"https://api.nasa.gov/EPIC/archive/natural/{year}/{month}/{day}/png/{image_name}.png?api_key={api_key}"
        try:
            img_data = requests.get(image_url).content
            filename = os.path.join("epic_images", f"epic_image_{i + 1}.png")
            with open(filename, 'wb') as f:
                f.write(img_data)
        except Exception as e:
            print(f"Не удалось загрузить {image_url}: {e}")

    with concurrent.futures.ThreadPoolExecutor() as executor:
        for i, item in enumerate(items[:count]):
            executor.submit(download, item, i)

my_api_key = "FtG0qQKlR5fFpInXojhXl96jyr9xPkFu0KHAtONA"
fetch_nasa_apod_images(my_api_key, count=30)
get_nasa_epic_image_url(my_api_key)
fetch_nasa_epic_images(my_api_key, count=10)

test_url = "https://example.com/txt/hello%20world.txt?v=9#python"
print("Расширение файла:", get_file_extension(test_url))  # Должно вывести: .txt