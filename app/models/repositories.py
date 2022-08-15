from typing import Callable, Tuple
from contextlib import AbstractContextManager
import logging
from datetime import date, datetime, timedelta

from dependency_injector.wiring import Provide, inject
from sqlalchemy.orm import Session

from bootstrap import Container
from app.models.db import Database
from .models import TelegramUserModel

class TelegramUserRepository():

    @inject
    def __init__(self, db: Database = Provide[Container.db]):
        self.session = db.session_singleton

    def get_user(self, chat_id: int, lang: str) -> TelegramUserModel:
        
        query = self.session.query(TelegramUserModel).filter(TelegramUserModel.chat_id == str(chat_id))
        if query.count() == 0:
            return None
        return query.first()
