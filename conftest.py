from datetime import datetime, timedelta
from unittest import mock
import pytest
import random

from adapters.rpc import URL_STATUS_OK
from bootstrap import Container
from models.db import Database
from models.models import SUBSCRIPTION_TRIAL, SubscriptionModel, TelegramUserModel, URLModel

from dependency_injector.providers import Configuration, Factory, Singleton

class MockContainer:

    def __init__(self):
        self.container = Container()

    def setup_storage(self, mock_storage=None):
        if mock_storage is None:
            mock_storage = mock.MagicMock()
        MockDatabase = mock.create_autospec(Database, spec_set=False)
        mock_db = MockDatabase(None, None)
        type(mock_db).session_singleton = mock.PropertyMock(return_value=mock_storage)
        self.container.db.override(mock_db)
        return self
    
    def setup_scraper(self, mock_scraper=None):
        if mock_scraper is None:
            mock_scraper = mock.MagicMock()
        self.container.rpc_scrap.override(Factory(mock_scraper))
        return self
    
    def install(self):
        self.container.wire(modules=[__name__], packages=['models', 'controllers', 'infra', 'core'])

class Helper:

    def get_mock_user(self, test_user_id=1, test_chat_id=1, test_lang='en', test_account_id=1):
        mock_user = mock.create_autospec(TelegramUserModel, instance=True)
        mock_user.id = test_user_id
        mock_user.chat_id = test_chat_id
        mock_user.lang = test_lang
        mock_user.account = test_account_id
        return mock_user

    def get_mock_subscription(self, subscription_id=1 , dt=None, dtStart=None, dtEnd=None,
                              account_id=None, kind=SUBSCRIPTION_TRIAL, active=True, is_active=True):

        if dt is None:
            now = datetime.utcnow()
            dt = now
        if dtStart is None:
            dtStart = dt
        if dtEnd is None:
            dtEnd = dtStart + timedelta(days=360)
        mock_subs = mock.create_autospec(SubscriptionModel, instance=True)
        mock_subs.id = subscription_id
        mock_subs.dt = dt
        mock_subs.dtStart = dtStart
        mock_subs.dtEnd = dtEnd
        mock_subs.account = account_id
        mock_subs.kind = kind
        mock_subs.active = active
        # Property override
        type(mock_subs).is_active = mock.PropertyMock(return_value=is_active)
        return mock_subs

    def get_scrap_data(self, test_url: str='https://as.com', test_domain: str='as.com', test_status: str='OK',
                       test_dt_expired: datetime=None):
        if test_dt_expired is None:
            test_dt_expired = datetime.utcnow() + timedelta(days=360)
        return {
        'url': test_url,
        'url_status': {
            'status': test_status,
            'domain': test_domain,
            'url': test_url,
            'response_time_in_ms': random.randint(10, 400)
        },
        'ssl_status': {
            'status': 'OK',
            'end': test_dt_expired.strftime('%Y-%m-%dT%H:%M:%SZ'),
            'domain': test_domain
        }
    }

    def get_mock_url(self, test_id=1, test_url: str='https://as.com', test_status: str=URL_STATUS_OK,
                     test_domain: int=1, test_dt: datetime=None, test_dtLastCheck: datetime=None):

        now = datetime.utcnow()
        if test_dt is None:
            test_dt = now
        if test_dtLastCheck is None:
            test_dtLastCheck = test_dt 
        mock_url = mock.create_autospec(URLModel, instance=True)
        mock_url.id = test_id
        mock_url.dt = test_dt
        mock_url.dtLastCheck = test_dtLastCheck
        mock_url.url = test_url
        mock_url.timeTakenMS = random.randint(50, 600)
        mock_url.status = test_status
        mock_url.domain = test_domain
        return mock_url

    def get_mock_user_account_urls(self, user=None):

        if user is None:
            user = self.get_mock_user()
        ret = []

        return ret


@pytest.fixture()
def scenery():

    yield MockContainer()

@pytest.fixture()
def dummy_trans():
    yield lambda x: x

@pytest.fixture()
def helper():
    yield Helper()
