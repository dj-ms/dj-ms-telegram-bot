from time import sleep

from app.bot.base import BaseBotWorker
from app.bot.decorators import bot_command, send_typing_action
from app.models import User


class Worker(BaseBotWorker):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user, self.user_created = User.get_user_and_created(self.update, self.context)

    @bot_command(name='start', description='🚀 Restart')
    def start(self) -> None:
        if self.user_created:
            text = f'Welcome, {self.user.first_name}!'
        else:
            text = f'Welcome back, {self.user.first_name}!'
        self.update.message.reply_text(text=text, reply_to_message_id=self.update.message.message_id)

    @bot_command(name='help', description='?? Help')
    @send_typing_action
    def help(self) -> None:
        sleep(3)
        self.update.message.reply_text(text='Help', reply_to_message_id=self.update.message.message_id)
