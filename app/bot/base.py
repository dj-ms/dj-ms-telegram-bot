from inspect import getmembers

from telegram import Update, BotCommand
from telegram.ext import CallbackContext

from app.bot.decorators import CommandMapper
from core.settings import LANGUAGES


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

    @classmethod
    def handle_command(cls, update, context):

        def command():
            self = cls(update, context)
            command_name = self.update.message.text.split()[0].replace('/', '')
            return getattr(self, command_name)()

        return command()

    @classmethod
    def get_commands(cls):
        return [_check_attr_name(method, name) for name, method in getmembers(cls, _is_command)]

    @classmethod
    def setup_commands(cls, bot):
        bot.delete_my_commands()
        language_codes = list(lang[0] for lang in LANGUAGES)
        for language_code in language_codes:
            bot.set_my_commands(
                language_code=language_code,
                commands=[
                    BotCommand(command.name, command.description) for command in cls.get_commands()
                ]
            )
