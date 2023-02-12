import logging
import sys
from inspect import getmembers

import telegram
from django.utils import translation
from telegram import Update, BotCommand, Bot
from telegram.ext import CallbackContext, CommandHandler

from app.bot.decorators import CommandMapper
from app.models import User
from core.settings import LANGUAGES, LANGUAGE_CODE, TELEGRAM_TOKEN

bot = Bot(TELEGRAM_TOKEN)
TELEGRAM_BOT_USERNAME = bot.get_me()["username"]
# Global variable - the best way I found to init Telegram bot
try:
    pass
except telegram.error.Unauthorized:
    logging.error("Invalid TELEGRAM_TOKEN.")
    sys.exit(1)


def _is_command(attr):
    return hasattr(attr, 'mapping') and isinstance(attr.mapping, CommandMapper)


def _check_attr_name(func, name):
    assert func.__name__ == name, (
        'Expected function (`{func.__name__}`) to match its attribute name '
        '(`{name}`). If using a decorator, ensure the inner function is '
        'decorated with `functools.wraps`, or that `{func.__name__}.__name__` '
        'is otherwise set to `{name}`.').format(func=func, name=name)
    return func


class BaseBotWorker:
    def __init__(self, update: Update, context: CallbackContext):
        self.update = update
        self.context = context
        self.user, self.user_created = User.get_user_and_created(self.update, self.context)
        self.set_language()

    @classmethod
    def handle_command(cls, update, context):

        def command():
            self = cls(update, context)
            command_name = self.update.message.text.split('@')[0].replace('/', '')
            return getattr(self, command_name)()

        return command()

    def set_language(self):
        language_code = self.user.language_code
        if language_code is None or language_code not in list(lang[0] for lang in LANGUAGES):
            language_code = LANGUAGE_CODE
        translation.activate(language_code)

    @classmethod
    def get_commands(cls):
        return [_check_attr_name(method, name) for name, method in getmembers(cls, _is_command)]

    @classmethod
    def setup_commands(cls, dispatcher, bot):
        commands = cls.get_commands()
        for command in commands:
            dispatcher.add_handler(CommandHandler(command.name, cls.handle_command))

        bot.delete_my_commands()
        language_codes = list(lang[0] for lang in LANGUAGES)
        for language_code in language_codes:
            bot.set_my_commands(
                language_code=language_code,
                commands=[
                    BotCommand(command.name, command.description) for command in commands
                ]
            )
