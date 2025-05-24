import os
import requests
import argparse
import concurrent.futures
from utils import get_file_extension
from utils import download_image
from dotenv import load_dotenv


def download_spacex_image(photo_url, i):
    ext = get_file_extension(photo_url) or ".jpg"
    filename = os.path.join("spacex_images", f"spacex_{i}{ext}")
    download_image(photo_url, filename)


def fetch_spacex_images(launch_id=None):
    base_url = "https://api.spacexdata.com/v5/launches"
    os.makedirs("spacex_images", exist_ok=True)
    if launch_id:
        url = f"{base_url}/{launch_id}"
        response = requests.get(url)
        response.raise_for_status()
        launches = [response.json()]
    else:
        response = requests.get(base_url)
        response.raise_for_status()
        launches = response.json()[::-1]

    for data in launches:
        photos = data.get("links", {}).get("flickr", {}).get("original", [])
        if photos:
            break
    else:
        print("Фото не найдены ни в одном из последних запусков.")
        return

    with concurrent.futures.ThreadPoolExecutor() as executor:
        for i, url in enumerate(photos, start=1):
            executor.submit(download_spacex_image, url, i)


def main():
    load_dotenv()

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--id", help="ID запуска SpaceX (если не указан – берётся последний)"
    )
    args = parser.parse_args()
    try:
        fetch_spacex_images(args.id)
    except requests.RequestException as e:
        print(f"Ошибка при получении изображений SpaceX: {e}")


if __name__ == "__main__":
    main()
