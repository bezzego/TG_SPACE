from urllib.parse import urlsplit, unquote
import os.path
import requests


def get_file_extension(url: str) -> str:
    path = urlsplit(url).path
    path = unquote(path)
    filename = os.path.split(path)[1]
    _, ext = os.path.splitext(filename)
    return ext


def download_image(url: str, filename: str, params=None):
    response = requests.get(url, params=params)
    response.raise_for_status()  # выбрасывает исключение, если HTTP-статус >= 400
    with open(filename, "wb") as f:
        f.write(response.content)
