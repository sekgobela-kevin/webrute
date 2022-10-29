from . import webapp
from . import generate

import webrute

import unittest
import threading


class BaseSetUpTests():
    _session_type = webrute.Session

    @classmethod
    def setUpClass(cls) -> None:
        # Webapp urls
        cls._webapp_url = "http://127.0.0.1:5000"
        cls._webapp_login_url = "http://127.0.0.1:5000/login"

        # Target to use when login in to weburl
        cls._login_target = {"url": cls._webapp_login_url, "method":"POST"}
        
        # This are records kept by webapp.
        cls._webapp_records = [
            {"username": "BROWN", "password":"1029384756"},
            {"username": "MARTINEZ", "password": "bigboss"},
            {"username": "ANDERSON", "password": "shuttle"},
            {"username": "THOMAS", "password": "titanium"},
            {"username": "JACKSON", "password": "underdog"}
        ]

        # Extracts passwords and usernames from webapp records.
        cls._webapp_usernames = {rec["username"] for rec in cls._webapp_records}
        cls._webapp_passwords = {rec["password"] for rec in cls._webapp_records}

        # Creates passwords and usernames containing those from webapp.
        # Created passwords and usernames are suporset of those from webapp.
        cls._passwords = generate.random_passwords(10, cls._webapp_passwords)
        cls._usernames = generate.random_passwords(10, cls._webapp_usernames)

        # Creates fields from passwords and usernames.
        cls._passwords_field = webrute.field("password", cls._passwords)
        cls._usernames_field = webrute.field("username", cls._usernames)

        # Creates table from fieds
        cls._table = webrute.table()
        cls._table.add_field(cls._passwords_field)
        cls._table.add_primary_field(cls._usernames_field)

    @staticmethod
    def record_trandformer(record):
        return webrute.transform_record(record, "POST")

    @property
    @staticmethod
    def callable_session(cls):
        return cls._session_type()

    @classmethod
    def tearDownClass(cls) -> None:
        pass

class SetUpTests(BaseSetUpTests, unittest.TestCase):
    _session_type = webrute.Session

    def setUp(self) -> None:
        super().setUp()
        self._session = self._session_type()
    
    def tearDown(self) -> None:
        super().tearDown()
        self._session.close()

    @staticmethod
    def success(response):
        content = response.read()
        if b"Login successful" in content:
            return True
        return False

    @staticmethod
    def failure(response):
        return b"Failed to login" in response.read()

class AsyncSetUpTests(BaseSetUpTests, unittest.IsolatedAsyncioTestCase):
    _session_type = webrute.AsyncSession

    async def asyncSetUp(self) -> None:
        await super().asyncSetUp()
        self._session = self._session_type()

    @staticmethod
    async def success(response):
        return SetUpTests.success(response)

    @staticmethod
    async def failure(response):
        return SetUpTests.failure(response)

    async def asyncTearDown(self) -> None:
        await super().asyncTearDown()
        await self._session.aclose()



def run_webapp():
    webapp.run(port=5000, threaded=True)
webappp_thread = threading.Thread(target=run_webapp)
webappp_thread.daemon = True
webappp_thread.start()
