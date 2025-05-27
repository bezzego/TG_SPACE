# Telegram Bot for NASA & SpaceX Image Posting 🚀🪐

Этот бот автоматически загружает изображения с открытых космических API (NASA APOD, NASA EPIC, SpaceX) и публикует их в Telegram-канал с заданным интервалом.

## 🚀 Возможности

- Получение последних изображений запусков SpaceX.
- Загрузка ежедневных снимков с NASA APOD.
- Получение снимков Земли с NASA EPIC.
- Публикация изображений в Telegram-канал.
- Задержка между публикациями настраивается.

## 📦 Установка

1. **Клонируйте репозиторий**:

   ```bash
   git clone https://github.com/ваш-юзернейм/ваш-репозиторий.git
   cd ваш-репозиторий
   ```

2. **Создайте и активируйте виртуальное окружение (опционально):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # или venv\Scripts\activate в Windows
   ```

3. **Установите зависимости:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Создайте файл `.env` в корне проекта со следующим содержимым:**

   ```
   TELEGRAM_BOT_TOKEN=ваш_токен_бота
   TELEGRAM_CHAT_ID=-100xxxxxxxxxx
   PUBLISH_DELAY_HOURS=4

   NASA_API_KEY=ваш_токен_с_сайта_NASA
   NASA_API_URL=https://api.nasa.gov/planetary/apod
   NASA_EPIC_URL=https://api.nasa.gov/EPIC/api/natural/images

   SPACEX_API_URL=https://api.spacexdata.com/v5/launches
   ```

## 🚀 Запуск

Для запуска бота:

```bash
python bot.py
```

Бот начнёт загружать изображения и публиковать их в Telegram-канал с заданной задержкой.

## 📁 Структура проекта

```
.
├── bot.py                  # Основной файл с Telegram-ботом
├── utils.py                # Вспомогательные функции (скачивание, сохранение, директории)
├── fetch_spacex_images.py  # Получение изображений из SpaceX API
├── fetch_apod_images.py    # Получение изображений из NASA APOD
├── fetch_epic_images.py    # Получение изображений из NASA EPIC
├── requirements.txt        # Зависимости проекта
└── .env                    # Настройки окружения (не добавляйте в git)
```

## 🛠 Используемые технологии

- Python 3.11+
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- NASA Open APIs
- SpaceX API

## ✅ Рекомендации

- Не забудьте добавить `.env` в `.gitignore`, чтобы не отправить токены в репозиторий.
- При изменении структуры, переменных или логики — не забудьте обновить README.md.
- Используйте `logging` или вывод в консоль для отслеживания статуса публикаций.

## 📬 Обратная связь

Если у вас есть предложения или баг-репорты — создавайте issue или отправьте Pull Request 🙌