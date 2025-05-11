import os
import requests
import argparse
import concurrent.futures
from utils import get_file_extension
from utils import download_image
from dotenv import load_dotenv

def download_spacex_image(photo_url, i):
    print(photo_url)
    ext = get_file_extension(photo_url) or ".jpg"
    filename = os.path.join("spacex_images", f"spacex_{i + 1}{ext}")
    download_image(photo_url, filename)

def fetch_spacex_images(base_url, launch_id=None):
    os.makedirs("spacex_images", exist_ok=True)
    if launch_id:
        url = f"{base_url}/{launch_id}"
        launches = [requests.get(url).json()]
    else:
        launches = requests.get(base_url).json()[::-1]

    for data in launches:
        photos = data.get("links", {}).get("flickr", {}).get("original", [])
        if photos:
            break
    else:
        print("Фото не найдены ни в одном из последних запусков.")
        return

    print(f"Название запуска: {data.get('name')}")
    print("Ссылки на фото:")

    with concurrent.futures.ThreadPoolExecutor() as executor:
        for i, url in enumerate(photos):
            executor.submit(download_spacex_image, url, i)

def main():
    load_dotenv()
    base_url = os.getenv("SPACEX_API_URL", "https://api.spacexdata.com/v5/launches")

    parser = argparse.ArgumentParser()
    parser.add_argument("--id", help="ID запуска SpaceX (если не указан – берётся последний)")
    args = parser.parse_args()
    try:
        fetch_spacex_images(base_url, args.id)
    except requests.RequestException as e:
        print(f"Ошибка при получении изображений SpaceX: {e}")

if __name__ == "__main__":
    main()