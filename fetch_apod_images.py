import os
from dotenv import load_dotenv
import requests
import concurrent.futures
from utils import get_file_extension


def main():
    load_dotenv()
    API_URL = os.getenv("NASA_API_URL")
    API_KEY = os.getenv("NASA_API_KEY")


    def fetch_apod_images(count=30):
        os.makedirs("apod_images", exist_ok=True)
        params = {"api_key": API_KEY, "count": count}

        try:
            response = requests.get(API_URL, params=params)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Ошибка запроса к APOD API: {e}")
            return

        items = response.json()

        def download(item, i):
            if item.get("media_type") != "image":
                return
            url = item.get("url")
            ext = get_file_extension(url) or ".jpg"
            try:
                img_data = requests.get(url).content
                filename = os.path.join("apod_images", f"apod_{i + 1}{ext}")
                with open(filename, 'wb') as f:
                    f.write(img_data)
            except Exception as e:
                print(f"Ошибка при скачивании {url}: {e}")

        with concurrent.futures.ThreadPoolExecutor() as executor:
            for i, item in enumerate(items):
                executor.submit(download, item, i)

    fetch_apod_images()

if __name__ == "__main__":
    main()