import os
import requests
import concurrent.futures
from utils import get_file_extension, download_image
from dotenv import load_dotenv
from urllib.parse import urlencode
from datetime import datetime


def download_epic_image(item, i, api_key):
    name = item["image"]
    date = datetime.fromisoformat(item["date"])
    year = date.strftime("%Y")
    month = date.strftime("%m")
    day = date.strftime("%d")
    img_url = f"https://api.nasa.gov/EPIC/archive/natural/{year}/{month}/{day}/png/{name}.png"
    params = {"api_key": api_key}

    filename = os.path.join("epic_images", f"epic_{i}.png")
    download_image(img_url, filename, params=params)


def fetch_epic_images(api_url, api_key, count=10):
    os.makedirs("epic_images", exist_ok=True)
    params = {"api_key": api_key}

    response = requests.get(api_url, params=params)
    response.raise_for_status()

    items = response.json()
    if not items:
        print("Нет данных EPIC.")
        return

    with concurrent.futures.ThreadPoolExecutor() as executor:
        for i, item in enumerate(items[:count], start=1):
            executor.submit(download_epic_image, item, i, api_key)


def main():
    try:
        API_URL = os.environ["NASA_EPIC_URL"]
        API_KEY = os.environ["NASA_API_KEY"]
        fetch_epic_images(API_URL, API_KEY)
    except requests.RequestException as e:
        print(f"Ошибка при получении изображений EPIC: {e}")


if __name__ == "__main__":
    load_dotenv()
    main()