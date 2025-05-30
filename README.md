# Космический Telegram-бот 🚀🪐

Бот автоматически загружает изображения с открытых космических API (NASA APOD, NASA EPIC, SpaceX) и публикует их в Telegram-канал с заданным интервалом.

## 🚀 Возможности

- Получение последних изображений запусков SpaceX
- Загрузка ежедневных снимков с NASA APOD
- Получение снимков Земли с NASA EPIC
- Публикация изображений в Telegram-канал
- Настраиваемая задержка между публикациями

## 📦 Установка

1. **Клонируйте репозиторий**:
   ```bash
   git clone https://github.com/ваш-юзернейм/ваш-репозиторий.git
   cd ваш-репозиторий
   ```

2. **Создайте и активируйте виртуальное окружение**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # для Windows: venv\Scripts\activate
   ```

3. **Установите зависимости**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Создайте файл `.env` со следующими параметрами**:
   ```
   TELEGRAM_BOT_TOKEN=ваш_токен_бота
   TELEGRAM_CHAT_ID=ваш_id_канала
   PUBLISH_DELAY_HOURS=4
   NASA_API_KEY=ваш_токен_с_сайта_NASA
   ```

## 🚀 Использование

### Загрузка изображений

1. **Загрузка снимков SpaceX**:
   ```bash
   python fetch_spacex_images.py  # загрузит фото последнего запуска
   python fetch_spacex_images.py --id 5eb87d47ffd86e000604b38a  # загрузит фото конкретного запуска
   ```

2. **Загрузка снимков NASA APOD**:
   ```bash
   python fetch_apod_images.py  # загрузит 30 случайных фото дня
   ```

3. **Загрузка снимков NASA EPIC**:
   ```bash
   python fetch_epic_images.py  # загрузит последние 10 снимков Земли
   ```

### Запуск бота

Для публикации загруженных изображений в Telegram-канал:
```bash
python bot.py  # использует папку epic_images по умолчанию
python bot.py путь_к_папке  # использует указанную папку
python bot.py --delay 2  # устанавливает задержку в 2 часа
```

## 📁 Структура проекта

```
.
├── bot.py                  # Основной файл бота
├── utils.py               # Вспомогательные функции
├── fetch_spacex_images.py # Загрузка фото SpaceX
├── fetch_apod_images.py   # Загрузка фото NASA APOD
├── fetch_epic_images.py   # Загрузка фото NASA EPIC
├── requirements.txt       # Зависимости проекта
└── .env                   # Настройки (не включать в git)
```

## 🛠 Требования

- Python 3.11+
- Токен Telegram-бота
- API-ключ NASA (получить на https://api.nasa.gov/)

## ⚠️ Важные замечания

- Добавьте `.env` в `.gitignore`
- Все изображения сохраняются в соответствующие папки: `spacex_images`, `apod_images`, `epic_images`
- Для работы бота требуется доступ к интернету