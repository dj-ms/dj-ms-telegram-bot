from django.utils.translation import gettext as _

from app.bot.base import BaseBotWorker
from app.bot.decorators import bot_command, send_typing_action, bot_menu


class Worker(BaseBotWorker):

    @bot_command(name='start', description=_('🚀 Restart'))
    @send_typing_action
    def start(self) -> None:
        self.clear_user_data()
        chat_type = self.update.message.chat.type
        if chat_type == 'private':
            if self.user_created:
                text = _('Welcome, %s!') % self.user.first_name
            else:
                text = _('Welcome back, %s!') % self.user.first_name
            kb = [
                [_('⚙️ Settings')],
            ]
            reply_markup = self.get_keyboard_markup(kb)
        else:
            text = _('Hi there! I am %s.') % self.context.bot.first_name
            reply_markup = None
        self.update.message.reply_text(text=text,
                                       reply_to_message_id=self.update.message.message_id,
                                       reply_markup=reply_markup)

    @bot_menu(name='settings', description=_('⚙️ Settings'))
    @bot_command(name='settings', description=_('⚙️ Settings'))
    @send_typing_action
    def settings(self) -> None:
        kb = [
            [_('🔙 Back')],
        ]
        reply_markup = self.get_keyboard_markup(kb)
        self.update.message.reply_text(text=_('Settings'),
                                       reply_to_message_id=self.update.message.message_id,
                                       reply_markup=reply_markup)
