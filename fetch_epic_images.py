import os
import requests
import concurrent.futures
from utils import get_file_extension, download_image
from dotenv import load_dotenv


def main():
    load_dotenv()
    API_URL = os.getenv("NASA_EPIC_URL")
    API_KEY = os.getenv("NASA_API_KEY")


    def fetch_epic_images(count=10):
        os.makedirs("epic_images", exist_ok=True)
        params = {"api_key": API_KEY}

        try:
            response = requests.get(API_URL, params=params)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Ошибка запроса к EPIC API: {e}")
            return

        items = response.json()
        if not items:
            print("Нет данных EPIC.")
            return


        def download(item, i):
            name = item["image"]
            date = item["date"].split()[0]
            year, month, day = date.split('-')
            img_url = f"https://api.nasa.gov/EPIC/archive/natural/{year}/{month}/{day}/png/{name}.png?api_key={API_KEY}"

            filename = os.path.join("epic_images", f"epic_{i + 1}.png")
            download_image(img_url, filename)


        with concurrent.futures.ThreadPoolExecutor() as executor:
            for i, item in enumerate(items[:count]):
                executor.submit(download, item, i)

    fetch_epic_images()

if __name__ == "__main__":
    main()