import gettext
import logging
import requests

from urllib.parse import urlparse

QUOTE_PROVIDER_URL = 'https://zenquotes.io/api/random'


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

def get_random_quote() -> str:

    try:
        response = requests.get(QUOTE_PROVIDER_URL)
        data = response.json()
        return data[0]['q']
    except:
        return "Opps Can't get quote"

_init_i18n()
