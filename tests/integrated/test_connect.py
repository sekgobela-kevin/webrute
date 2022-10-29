from . import setup_tests

import webrute
import httpx
import unittest


class TestConnect(setup_tests.SetUpTests):
    def test_connector(self):
        record = webrute.transform_record(self._webapp_records[0], "POST")

        # Performs request without session
        response = webrute.connector(self._webapp_url, record)
        self.assertIsInstance(response, httpx.Response)
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.url, self._webapp_url)

        target = {"url":self._webapp_url, "method":"POST"}
        response = webrute.connector(target, record)
        self.assertEqual(response.request.method, "POST")

    def test_connector_session(self):
        record = webrute.transform_record(self._webapp_records[0], "POST")
        with webrute.Session() as session:
            response = webrute.connector(self._webapp_url, record, session)
            self.assertIsInstance(response, httpx.Response)
            self.assertFalse(session.is_closed)

        # response = webrute.connector(self._webapp_url, record, webrute.Session)
        # self.assertIsInstance(response, httpx.Response)


class TestAsyncConnect(setup_tests.AsyncSetUpTests):
    async def test_connector(self):
        record = webrute.transform_record(self._webapp_records[0], "POST")

        # Performs request without session
        response = await webrute.async_connector(self._webapp_url, record)
        self.assertIsInstance(response, httpx.Response)
        self.assertEqual(response.request.method, "GET")
        self.assertEqual(response.request.url, self._webapp_url)

        target = {"url":self._webapp_url, "method":"POST"}
        response = await webrute.async_connector(target, record)
        self.assertEqual(response.request.method, "POST")

    async def test_connector_session(self):
        record = webrute.transform_record(self._webapp_records[0], "POST")
        async with webrute.AsyncSession() as session:
            response = await webrute.async_connector(
                self._webapp_url, record, session)
            self.assertIsInstance(response, httpx.Response)
            self.assertFalse(session.is_closed)

        # response = await webrute.async_connector(
        #     self._webapp_url, record, webrute.AsyncSession)
        # self.assertIsInstance(response, httpx.Response)
            

if __name__ == "__main__":
    unittest.main()

