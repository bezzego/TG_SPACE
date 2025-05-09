import os
import requests
import argparse
import concurrent.futures
from utils import get_file_extension

def fetch_spacex_images(launch_id=None):
    os.makedirs("spacex_images", exist_ok=True)
    if launch_id:
        url = f"https://api.spacexdata.com/v5/launches/{launch_id}"
        launches = [requests.get(url).json()]
    else:
        launches = requests.get("https://api.spacexdata.com/v5/launches").json()[::-1]

    for data in launches:
        photos = data.get("links", {}).get("flickr", {}).get("original", [])
        if photos:
            break
    else:
        print("Фото не найдены ни в одном из последних запусков.")
        return

    print(f"Название запуска: {data.get('name')}")
    print("Ссылки на фото:")

    def download(photo_url, i):
        try:
            print(photo_url)
            ext = get_file_extension(photo_url) or ".jpg"
            img_data = requests.get(photo_url).content
            filename = os.path.join("spacex_images", f"spacex_{i + 1}{ext}")
            with open(filename, 'wb') as f:
                f.write(img_data)
        except Exception as e:
            print(f"Ошибка при скачивании {photo_url}: {e}")

    with concurrent.futures.ThreadPoolExecutor() as executor:
        for i, url in enumerate(photos):
            executor.submit(download, url, i)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", help="ID запуска SpaceX (если не указан – берётся последний)")
    args = parser.parse_args()
    fetch_spacex_images(args.id)