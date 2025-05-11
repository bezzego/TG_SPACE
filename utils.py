from urllib.parse import urlsplit, unquote
import os.path
import requests

def get_file_extension(url: str) -> str:
    path = urlsplit(url).path
    path = unquote(path)
    filename = os.path.split(path)[1]
    _, ext = os.path.splitext(filename)
    return ext

def download_image(url: str, filename: str):
    try:
        img_data = requests.get(url).content
        with open(filename, 'wb') as f:
            f.write(img_data)
    except Exception as e:
        print(f"Ошибка при скачивании {url}: {e}")