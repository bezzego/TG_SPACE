from telegram.ext import Updater, CommandHandler
from telegram import Bot


def start(update, context):
    user = update.effective_user
    print(user.to_dict())  # {'id': ..., 'first_name': ..., 'username': ..., ...}
    update.message.reply_text('Привет!')

def main():
    token = "8190245623:AAEDkdSHOsly1cgyiN6ON0H_J9H9vunB-3U"
    chat_id = "-1002561858696"
    text = "Привет подписчикам! 🚀 Вот оно — первое сообщение от Python-бота."

    bot = Bot(token=token)
    bot.send_message(chat_id=chat_id, text=text)
    with open("epic_images/epic_1.png", "rb") as photo:        bot.send_photo(chat_id=chat_id, photo=photo, caption="Смотрите, какая красота!")

if __name__ == "__main__":
    main()