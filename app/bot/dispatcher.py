"""
    Telegram event handlers
"""
from queue import Queue

from python_telegram_bot_django_persistence.persistence import DjangoPersistence
from telegram.ext import (
    Dispatcher, MessageHandler, Filters, )

from app.bot.base import bot
from app.bot.workers.example_main import Worker
from core.settings import DEBUG


def setup_dispatcher(dp):
    """
    Adding handlers for events from Telegram
    """

    Worker.setup_commands(dp, dp.bot)
    dp.add_handler(MessageHandler(Filters.text, Worker.handle_menu))

    # EXAMPLES FOR HANDLERS
    # dp.add_handler(MessageHandler(Filters.text, <function_handler>))
    # dp.add_handler(MessageHandler(
    #     Filters.document, <function_handler>,
    # ))
    # dp.add_handler(CallbackQueryHandler(<function_handler>, pattern="^r\d+_\d+"))
    # dp.add_handler(MessageHandler(
    #     Filters.chat(chat_id=int(TELEGRAM_FILESTORAGE_ID)),
    #     # & Filters.forwarded & (Filters.photo | Filters.video | Filters.animation),
    #     <function_handler>,
    # ))

    return dp


n_workers = 1 if DEBUG else 4
dispatcher = setup_dispatcher(Dispatcher(bot, update_queue=Queue(100),
                                         workers=n_workers, persistence=DjangoPersistence()))
