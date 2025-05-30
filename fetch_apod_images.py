import os
from dotenv import load_dotenv
import requests
import concurrent.futures
from utils import get_file_extension, download_image


def download_apod_image(item, i):
    if item.get("media_type") != "image":
        return
    url = item.get("url")
    ext = get_file_extension(url) or ".jpg"
    filename = os.path.join("apod_images", f"apod_{i}{ext}")
    download_image(url, filename)


def fetch_apod_images(api_key, count=30):
    api_url = "https://api.nasa.gov/planetary/apod"
    os.makedirs("apod_images", exist_ok=True)
    params = {"api_key": api_key, "count": count}

    response = requests.get(api_url, params=params)
    response.raise_for_status()

    items = response.json()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        for i, item in enumerate(items, start=1):
            executor.submit(download_apod_image, item, i)


def main():
    load_dotenv()
    api_key = os.environ["NASA_API_KEY"]

    try:
        fetch_apod_images(api_key)
    except requests.RequestException as e:
        print(f"Ошибка при получении изображений: {e}")


if __name__ == "__main__":
    main()
