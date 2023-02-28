import logging
import sys
from inspect import getmembers
from typing import Iterable

import telegram
from django.utils import translation
from django.utils.translation import gettext as _
from telegram import Update, BotCommand, Bot
from telegram.ext import CallbackContext, CommandHandler

from app.bot.decorators import CommandMapper, MenuMapper, bot_menu, send_typing_action
from app.models import User
from core.settings import LANGUAGES, TELEGRAM_TOKEN

bot = Bot(TELEGRAM_TOKEN)
TELEGRAM_BOT_USERNAME = bot.get_me()["username"]
# Global variable - the best way I found to init Telegram bot
try:
    pass
except telegram.error.Unauthorized:
    logging.error("Invalid TELEGRAM_TOKEN.")
    sys.exit(1)


def _is_command(attr):
    return hasattr(attr, 'command_mapping') and isinstance(attr.command_mapping, CommandMapper)


def _is_menu(attr):
    return hasattr(attr, 'menu_mapping') and isinstance(attr.menu_mapping, MenuMapper)


def _check_attr_name(func, name):
    assert func.__name__ == name, (
        'Expected function (`{func.__name__}`) to match its attribute name '
        '(`{name}`). If using a decorator, ensure the inner function is '
        'decorated with `functools.wraps`, or that `{func.__name__}.__name__` '
        'is otherwise set to `{name}`.').format(func=func, name=name)
    return func


def flatten(xs):
    for x in xs:
        if isinstance(x, Iterable) and not isinstance(x, (str, bytes)):
            yield from flatten(x)
        else:
            yield x


class BaseBotWorker:
    def __init__(self, update: Update, context: CallbackContext):
        self.update = update
        self.context = context
        self.user, self.user_created = User.get_user_and_created(self.update, self.context)

    @classmethod
    def get_commands(cls):
        return [_check_attr_name(method, name) for name, method in getmembers(cls, _is_command)]

    @classmethod
    def setup_commands(cls, dispatcher, bot_instance):
        commands = cls.get_commands()
        for command in commands:
            dispatcher.add_handler(CommandHandler(command.name, cls.handle_command))
        bot_instance.delete_my_commands()
        language_codes = list(lang[0] for lang in LANGUAGES)
        for language_code in language_codes:
            with translation.override(language_code):
                bot_commands = list(BotCommand(command.name, _(command.description)) for command in commands)
            bot_instance.set_my_commands(language_code=language_code, commands=bot_commands)

    @classmethod
    def handle_command(cls, update, context):
        self = cls(update, context)
        next_path = self.update.message.text.split('@')[0].replace('/', '')
        self.__update_paths(next_path)
        command = getattr(self, next_path)
        with translation.override(self.user.language_code):
            return command()

    @classmethod
    def handle_menu(cls, update, context):
        self = cls(update, context)
        input_text = self.update.message.text
        avail_menus = getmembers(cls, _is_menu)
        with translation.override(self.user.language_code):
            avail_menu_names = list(_(func.description) for name, func in avail_menus)
            if input_text in avail_menu_names:
                next_path = next(name for name, func in avail_menus if _(func.description) == input_text)
                args = ()
            else:
                next_path = self.context.user_data.get('path', 'start')
                args = (input_text, )
            self.__update_paths(next_path)
            try:
                menu = getattr(self, next_path)
                return menu(*args)
            except AssertionError as e:
                logging.error(e)

    def __update_paths(self, next_path):
        current_path = self.context.user_data.get('path', 'start')
        prev_path = self.context.user_data.get('last_path', 'start')
        self.context.user_data.update({
            'path': next_path,
            'last_path': current_path,
            'prev_path': prev_path
        })

    def get_keyboard_markup(self, kb, resize_keyboard=True, one_time_keyboard=False, **kwargs):
        buttons_list = list(flatten(kb))
        self.context.user_data.update({'keyboard': buttons_list})
        return telegram.ReplyKeyboardMarkup(kb, resize_keyboard=resize_keyboard,
                                            one_time_keyboard=one_time_keyboard, **kwargs)

    def send_message(self, chat_id, text, reply_markup=None, parse_mode='HTML', **kwargs):
        return self.context.bot.send_message(chat_id=chat_id, text=_(text), reply_markup=reply_markup,
                                             parse_mode='HTML', **kwargs)

    def clear_user_data(self):
        self.context.user_data.clear()
        self.context.user_data['path'] = 'start'
        self.context.user_data['keyboard'] = []
