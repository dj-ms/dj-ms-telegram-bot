import os, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from telegram import Bot
from telegram.ext import Updater

from core.settings import TELEGRAM_TOKEN
from app.bot.dispatcher import setup_dispatcher


def run_polling(tg_token: str = TELEGRAM_TOKEN):
    """ Run bot in polling mode """
    updater = Updater(tg_token, use_context=True)

    setup_dispatcher(updater.dispatcher)

    bot_info = Bot(tg_token).get_me()
    bot_link = f"https://t.me/{bot_info['username']}"

    print(f"Polling of '{bot_link}' has started")
    # it is really useful to send '👋' emoji to developer
    # when you run local test
    # bot.send_message(text='👋', chat_id=<YOUR TELEGRAM ID>)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    run_polling()
