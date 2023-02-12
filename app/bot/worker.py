from app.bot.base import BaseBotWorker
from app.bot.decorators import bot_command
from app.models import User


class Worker(BaseBotWorker):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user, self.user_created = User.get_user_and_created(self.update, self.context)

    @bot_command(name='start')
    def start(self) -> None:

        if self.user_created:
            text = f'Welcome, {self.user.first_name}!'
        else:
            text = f'Welcome back, {self.user.first_name}!'

        self.update.message.reply_text(text=text)
