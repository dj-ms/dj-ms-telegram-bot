from django.utils import translation
from django.utils.translation import gettext as _

from app.bot.base import BaseBotWorker
from app.bot.decorators import bot_command, send_typing_action, bot_menu
from core.settings import LANGUAGES, LANGUAGE_CODE


class Worker(BaseBotWorker):

    @bot_command(name='start', description=_('🚀 Restart'))
    @send_typing_action
    def start(self, *args) -> None:
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
    def settings(self, *args) -> None:
        kb = [
            [_('🔙 Back')],
            [_('🌐 Language')],
        ]
        reply_markup = self.get_keyboard_markup(kb)
        self.update.message.reply_text(text=_('Settings'),
                                       reply_to_message_id=self.update.message.message_id,
                                       reply_markup=reply_markup)

    @bot_menu(name='language', description=_('🌐 Language'))
    @bot_command(name='language', description=_('🌐 Language'))
    @send_typing_action
    def language(self, language_code: str = None) -> None:
        if language_code is not None:
            if language_code not in list(lang[1] for lang in LANGUAGES):
                language_code = LANGUAGE_CODE
            language_code = next(lang[0] for lang in LANGUAGES if lang[1] == language_code)
            self.user.language_code = language_code
            self.user.save()
            print(self.user.language_code)
            translation.activate(language_code)
            self.update.message.reply_text(text=_('Language changed to %s') % language_code,
                                           reply_to_message_id=self.update.message.message_id)
            return self.start()
        kb = [
            [_('🔙 Back')],
            list(str(lang[1]) for lang in LANGUAGES)
        ]
        reply_markup = self.get_keyboard_markup(kb)
        self.update.message.reply_text(text=_('Language'),
                                       reply_to_message_id=self.update.message.message_id,
                                       reply_markup=reply_markup)
