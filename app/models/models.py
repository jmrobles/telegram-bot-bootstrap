from __future__ import annotations

from datetime import datetime
from enum import Enum
from http.client import NOT_FOUND

from dependency_injector.wiring import Provide, inject

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean



from .db import Base, ChoiceType, Database #, session

class TelegramUserModel(Base):

    __tablename__ = 'telegram_user'

    id = Column(Integer, primary_key=True)
    chat_id = Column(String, unique=True)
    lang = Column(String, default='en')

    
    def __repr__(self):
        return '<TelegramUserModel %r>' % self.chat_id
    
    def __str__(self):
        return self.chat_id
