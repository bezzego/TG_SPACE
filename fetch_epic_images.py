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
    img_url = (
        f"https://api.nasa.gov/EPIC/archive/natural/{year}/{month}/{day}/png/{name}.png"
    )
    params = {"api_key": api_key}

    filename = os.path.join("epic_images", f"epic_{i}.png")
    query_string = urlencode(params)
    full_url = f"{img_url}?{query_string}"
    download_image(full_url, filename)


def fetch_epic_images(api_key, count=10):
    api_url = "https://api.nasa.gov/EPIC/api/natural"
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
    load_dotenv()
    api_key = os.environ["NASA_API_KEY"]
    try:
        fetch_epic_images(api_key)
    except requests.RequestException as e:
        print(f"Ошибка при получении изображений EPIC: {e}")


if __name__ == "__main__":
    main()
