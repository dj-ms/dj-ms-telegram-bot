import re

from django.utils import translation
from django.utils.translation import gettext as _

from app.bot.base import BaseBotWorker
from app.bot.decorators import bot_command, send_typing_action, bot_menu
from core.settings import LANGUAGES, LANGUAGE_CODE


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


class Worker(BaseBotWorker):

    @bot_command(name='start', description=_('🚀 Restart'))
    @send_typing_action
    def start(self, *args) -> None:
        self.clear_user_data()
        chat_type = self.update.message.chat.type
        if chat_type == 'private':
            if self.user_created:
                text = _('Welcome, <b>%s</b>!') % self.user.first_name
            else:
                text = _('Welcome back, <b>%s</b>!') % self.user.first_name
            kb = [[_('⚙️ Settings')], ]
            reply_markup = self.get_keyboard_markup(kb)
        else:
            text = _('Hi there! I am <b>%s</b>.') % self.context.bot.first_name
            reply_markup = None
        self.send_message(self.update.message.chat.id, text=str(text), reply_markup=reply_markup)

    @bot_menu(name='home', description=_('🏠 Home'))
    @send_typing_action
    def home(self, *args) -> None:
        return self.start()

    @bot_menu(name='back', description='🔙 Back')
    @send_typing_action
    def back(self) -> None:
        prev_path = self.context.user_data.get('prev_path', 'start')
        self.context.user_data.update({'path': prev_path})
        getattr(self, prev_path)()

    @bot_menu(name='settings', description=_('⚙️ Settings'))
    @bot_command(name='settings', description=_('⚙️ Settings'))
    @send_typing_action
    def settings(self, *args) -> None:
        kb = [
            [_('🔙 Back'), _('🏠 Home')],
            [_('🌐 Language'), _('👤 Change name')],
        ]
        reply_markup = self.get_keyboard_markup(kb)
        text = _('This is settings menu.\nChoose what you want to change.')
        self.send_message(self.update.message.chat.id, text=text, reply_markup=reply_markup)

    @bot_menu(name='language', description=_('🌐 Language'))
    @bot_command(name='language', description=_('🌐 Language'))
    @send_typing_action
    def language(self, language_name: str = None) -> None:
        if language_name is not None:
            if language_name in list(_(lang[1]) for lang in LANGUAGES):
                language_code = next(lang[0] for lang in LANGUAGES if language_name == _(lang[1]))
            else:
                language_code = LANGUAGE_CODE
            self.user.language_code = language_code
            self.user.save()
            lang_name = next(lang[1] for lang in LANGUAGES if _(lang[0]) == language_code)
            with translation.override(language_code):
                self.send_message(self.update.message.chat.id, text=_('Language changed to <b>%s</b>.') % lang_name)
                return self.start()
        languages = list(str(lang[1]) for lang in LANGUAGES if lang[0] != self.user.language_code)
        kb = [[_('🔙 Back')], *list(chunks(languages, 3))]
        reply_markup = self.get_keyboard_markup(kb)
        lang_name = next(lang[1] for lang in LANGUAGES if _(lang[0]) == self.user.language_code)
        text = _('Choose preferred language from the list below. '
                 'Your current language is <b>%s</b>.') % lang_name
        self.send_message(self.update.message.chat.id, text=text, reply_markup=reply_markup)

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
                self.send_message(self.update.message.chat.id, text=_('Your name changed to <b>%s</b>.') % new_name_str)
                return self.start()
        kb = [[_('🔙 Back')], ]
        reply_markup = self.get_keyboard_markup(kb)
        text = _('Enter your name in one of the following formats:\n'
                 ' - <b><i>John</i></b>\n'
                 ' - <b><i>John Smith</i></b>\n'
                 ' - <b><i>John S. Smith</i></b>\n'
                 ' - <b><i>John Smith Smith</i></b>')
        self.send_message(self.update.message.chat.id, text=text, reply_markup=reply_markup)
