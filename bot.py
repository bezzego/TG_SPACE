from telegram.error import TelegramError
import os
import time
import random
import argparse
from telegram import Bot
from PIL import Image
from dotenv import load_dotenv


DEFAULT_DELAY_HOURS = 4
MAX_FILE_SIZE_MB = 20


def compress_image(path, max_size_mb=20):
    temp_path = f"temp_{os.path.basename(path)}"
    with Image.open(path) as image:
        image.save(temp_path, optimize=True, quality=85)
        if os.path.getsize(temp_path) <= max_size_mb * 1024 * 1024:
            return temp_path
        image.save(temp_path, optimize=True, quality=65)
        return temp_path



def get_image_files(directory):
    return [os.path.join(directory, f) for f in os.listdir(directory)
            if f.lower().endswith(('.jpg', '.jpeg', '.png'))]


def publish_photo(bot, chat_id, photo_path):
    if os.path.getsize(photo_path) > MAX_FILE_SIZE_MB * 1024 * 1024:
        print(f"{photo_path} слишком большой, пытаюсь сжать...")
        photo_path = compress_image(photo_path)
    with open(photo_path, 'rb') as photo:
        bot.send_photo(chat_id=chat_id, photo=photo)
    print(f"Опубликовано: {photo_path}")


def publish_photos(directory, token, chat_id, delay_hours):
    bot = Bot(token=token)
    while True:
        photos = get_image_files(directory)
        if not photos:
            print("В директории нет изображений.")
            time.sleep(delay_hours * 3600)
            continue

        random.shuffle(photos)

        for photo_path in photos:
            try:
                publish_photo(bot, chat_id, photo_path)
            except (OSError, IOError, ValueError, TelegramError) as e:
                print(f"Ошибка при публикации {photo_path}: {e}")
            time.sleep(delay_hours * 3600)


def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description="Автоматическая публикация изображений в Telegram-канал.")
    parser.add_argument("directory", nargs='?', default="epic_images")
    parser.add_argument("--delay", type=float, default=float(os.getenv("PUBLISH_DELAY_HOURS", DEFAULT_DELAY_HOURS)))
    parser.add_argument("--token", default=os.environ["TELEGRAM_BOT_TOKEN"])
    parser.add_argument("--chat-id", default=os.environ["TELEGRAM_CHAT_ID"])

    args = parser.parse_args()
    publish_photos(args.directory, args.token, args.chat_id, args.delay)


if __name__ == "__main__":
    main()