


## Автоматическая публикация фото в Telegram-канал

Скрипт `bot.py` публикует фото из указанной директории в Telegram-канал с заданной периодичностью.

### Как настроить

1. Установите зависимости:
   ```
   pip install -r requirements.txt
   ```

2. Создайте файл `.env` в корне проекта со следующим содержимым:
   ```
   TELEGRAM_BOT_TOKEN=ваш_токен_бота
   TELEGRAM_CHAT_ID=-100xxxxxxxxxx
   PUBLISH_DELAY_HOURS=4
   ```

3. Убедитесь, что в директории `epic_images` (или любой другой) есть изображения в формате `.jpg`, `.jpeg` или `.png`.


4. Запустите скрипт:
   ```
   python bot.py
   ```

Скрипт будет публиковать изображения по одному каждые 4 часа (или другой интервал, заданный через `PUBLISH_DELAY_HOURS`).

### Примеры запуска всех скриптов

- Публикация фото из папки в Telegram-канал:
  ```
  python bot.py
  ```

- Загрузка фото NASA APOD:
  ```
  python fetch_apod.py
  ```

- Загрузка фото NASA EPIC:
  ```
  python fetch_epic.py
  ```

- Загрузка фото с последнего запуска SpaceX:
  ```
  python fetch_spacex.py
  ```

- Загрузка фото с конкретного запуска SpaceX по ID:
  ```
  python fetch_spacex.py --id <launch_id>
  ```