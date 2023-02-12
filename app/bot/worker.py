from django.utils.translation import gettext as _

from app.bot.base import BaseBotWorker, TELEGRAM_BOT_USERNAME
from app.bot.decorators import bot_command, send_typing_action


class Worker(BaseBotWorker):

    @bot_command(name='start', description=_('🚀 Restart'))
    @send_typing_action
    def start(self) -> None:
        chat_type = self.update.message.chat.type
        if chat_type == 'private':
            if self.user_created:
                text = _('Welcome, %s!') % self.user.first_name
            else:
                text = _('Welcome back, %s!') % self.user.first_name
        else:
            text = _('Hi there! I am %s.') % self.context.bot.first_name
        self.update.message.reply_text(text=text, reply_to_message_id=self.update.message.message_id)
