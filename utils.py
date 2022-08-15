import gettext
import logging

from urllib.parse import urlparse


def get_trans(lang_code: str):
    """
    Get the translator for the language
    """
    lang_code = lang_code if lang_code == 'es' or lang_code == 'en' else 'en'
    return _map_trans.get(lang_code).gettext

# Private
_map_trans = {
    'es': None,
    'en': None
}

def _init_i18n():
    """
    Initialize the translators
    """
    _map_trans['es'] = gettext.translation('messages', localedir='locales', languages=('es',))
    _map_trans['en'] = gettext.translation('messages', localedir='locales', languages=('en',))

_init_i18n()
