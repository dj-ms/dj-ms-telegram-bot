from telegram import Update

from core.celery import app


@app.task(ignore_result=True)
def process_telegram_event(update_json):
    from app.bot.base import bot
    update = Update.de_json(update_json, bot)
    from app.bot.dispatcher import dispatcher
    dispatcher.process_update(update)
