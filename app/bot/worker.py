import re

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

    @bot_menu(name='home', description=_('🏠 Home'))
    @send_typing_action
    def home(self, *args) -> None:
        return self.start()

    @bot_menu(name='settings', description=_('⚙️ Settings'))
    @bot_command(name='settings', description=_('⚙️ Settings'))
    @send_typing_action
    def settings(self, *args) -> None:
        kb = [
            [_('🔙 Back'), _('🏠 Home')],
            [_('🌐 Language'), _('👤 Change name')],
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

    @bot_menu(name='change_name', description=_('👤 Change name'))
    @send_typing_action
    def change_name(self, new_name_str: str = None) -> None:
        if new_name_str is not None:
            if match := re.search(r'(?P<first>[\w|-]{1,64})( (?P<middle>[\w|-]{1,64})( (?P<last>[\w|-]{1,64}))?)?',
                                  new_name_str):
                first_name = match.group('first')
                if match.group('middle') and match.group('last'):
                    first_name += ' ' + match.group('middle')
                    last_name = match.group('last')
                else:
                    last_name = match.group('middle')
                self.user.first_name = first_name
                self.user.last_name = last_name
                self.user.save()
                self.update.message.reply_text(text=_('Name changed to %s') % new_name_str,
                                               reply_to_message_id=self.update.message.message_id)
                return self.start()
        kb = [
            [_('🔙 Back')],
        ]
        reply_markup = self.get_keyboard_markup(kb)
        self.update.message.reply_text(text=_('Change name'),
                                       reply_to_message_id=self.update.message.message_id,
                                       reply_markup=reply_markup)
