from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from app.models.db import Database
from core.tg_bot import ITGBot

class Container(DeclarativeContainer):
    
    conf = providers.Configuration()
    db = providers.Singleton(Database, conf.db_url, conf.db_echo)
    bot = providers.AbstractSingleton(ITGBot, conf.tg_bot_token)
