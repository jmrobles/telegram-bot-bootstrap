from contextlib import contextmanager, AbstractContextManager
import logging
from typing import Callable

from sqlalchemy import create_engine
from sqlalchemy import orm
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy.types as types

# engine = create_engine('sqlite:///db.sqlite?check_same_thread=False', echo=True)

# Session = sessionmaker(bind=engine)
# session = Session()

Base = declarative_base()


class ChoiceType(types.TypeDecorator):
    impl = types.Integer

    def __init__(self, choices, *args, **kwargs):
        self.choices = {k: v for k, v in enumerate(choices)}
        super(ChoiceType, self).__init__(*args, **kwargs)

    def process_bind_param(self, value, dialect):
        return [k for k, v in self.choices.items() if v == value][0]

    def process_result_value(self, value, dialect):
        return self.choices.get(value)

class Database:

    def __init__(self, db_url: str, echo: str) -> None:
        self._engine = create_engine(db_url, echo=echo == 'True')
        self._session_factory = orm.scoped_session(
            orm.sessionmaker(
                autocommit=False,
                autoflush=False,
                expire_on_commit=True,
                bind=self._engine,
            ),
        )
        self.session_singleton = self._session_factory()

    def create_database(self) -> None:
        Base.metadata.create_all(self._engine)

    @contextmanager
    def session(self) -> Callable[..., AbstractContextManager[Session]]:
        session: Session = self._session_factory()
        try:
            yield session
        except Exception:
            logging.exception("Session rollback because of exception")
            session.rollback()
            raise
        finally:
            session.close()
