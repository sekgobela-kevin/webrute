from webrute import _functions
import webrute

import httpx
import inspect
import unittest


class TestSetUp():
    _session_type = None

    def setUp(self) -> None:
        self._target_reached_response = httpx.Response(200, 
            text="target reached")
        self._success_response = httpx.Response(200, text="success")
        self._failure_response = httpx.Response(200, text="failure")
        self._error_response = httpx.Response(400, text="error")
        
        self._target = ""
        self._record = webrute.record({"data":{"pass":12, "name":"ttr"}})
        self._session = self._session_type()


class Test(TestSetUp, unittest.TestCase):
    _session_type = httpx.Client

    def test_setUp(self) -> None:
        super().setUp()

    def test_connector(self):
        with self.assertRaises(httpx.UnsupportedProtocol):
            _functions.connector(self._target, self._record)
        with self.assertRaises(httpx.UnsupportedProtocol):
            _functions.connector(self._target, self._record, self._session)
        with self.assertRaises(TypeError):
            _functions.connector(self._target, {"pass":4, "name":"ttr"})


    def test_target_reached(self):
        self.assertTrue(_functions.target_reached(self._success_response))
        self.assertFalse(_functions.target_reached(self._error_response))


    def test_target_error(self):
        self.assertFalse(_functions.target_error(self._success_response))
        self.assertTrue(_functions.target_error(self._error_response))


    def test_transform_record(self):
        self.assertEqual(_functions.transform_record({"pass":3}, ""), 
            {"pass":3})
        self.assertEqual(_functions.transform_record({"pass":3}, "GET"), 
            {"params": {"pass":3}})
        self.assertEqual(_functions.transform_record({"pass":3}, "POST"), 
            {"data": {"pass":3}})

    def test_transform_target(self):
        self.assertDictEqual(_functions.transform_target("example.com"),
            {"url": "example.com", "method": "GET"})
        self.assertDictEqual(_functions.transform_target({"url": "example.com"}),
            {"url": "example.com"})


    def test_transform_connector_arguments(self):
        self.assertDictEqual(_functions.transform_connector_arguments(
            {"pass": 300}), {"pass": 300}
        )
        self.assertDictEqual(_functions.transform_connector_arguments(
            {"url": "example.com"}),
            {"url": "example.com", "method":"GET"}
        )
        self.assertDictEqual(_functions.transform_connector_arguments(
            {"url": "example.com", "data":{}}),
            {"url": "example.com", "data":{}, "method":"POST"}
        )

    def test_guess_connector_method(self, methods=("GET", "POST")):
        self.assertEqual(_functions.guess_connector_method({"pass": 300}),
            None)
        self.assertEqual(_functions.guess_connector_method(
            {"url": "example.com"}), "GET")
        self.assertEqual(_functions.guess_connector_method(
            {"url": "example.com", "content":b""}), "POST")

    def test_create_connector_arguments(self):
        self.assertDictEqual(_functions.create_connector_arguments(
            {"url": "example.com"}, {"url":"example.org","pass":12}),
            {"url":"example.org", "pass":12}
        )

        


    def test_create_session(self):
        with _functions.create_session({"headers":{}}) as session:
            self.assertIsInstance(session, httpx.Client)
        with httpx.Client() as session:
            session_ = _functions.create_session(session)
            self.assertEqual(session_, session)


    def test_setup_session(self):
        with _functions.setup_session(None) as session:
            self.assertIsInstance(session, httpx.Client)


    def test_session_closer(self):
        with httpx.Client() as session:
            _functions.session_closer(session)
            self.assertTrue(session.is_closed)


class AsyncTest(TestSetUp, unittest.IsolatedAsyncioTestCase):
    _session_type = httpx.AsyncClient

    async def async_connector(self):
        with self.assertRaises(httpx.UnsupportedProtocol):
            await _functions.connector(self._target, self._record)
        with self.assertRaises(httpx.UnsupportedProtocol):
            await _functions.connector(self._target, self._record, self._session)
        with self.assertRaises(TypeError):
            await _functions.connector(self._target, {"pass":4, "name":"ttr"})

    async def async_target_reached(self):
        self.assertTrue(await _functions.target_reached(self._success_response))
        self.assertFalse(await _functions.target_reached(self._error_response))

    async def test_async_target_error(self):
        self.assertFalse(await _functions.async_target_error(self._success_response))
        self.assertTrue(await _functions.async_target_error(self._error_response))

    async def test_create_async_session(self):
        async with _functions.create_async_session({"headers":{}}) as session:
            self.assertIsInstance(session, httpx.AsyncClient)
        async with httpx.AsyncClient() as session:
            session_ = _functions.create_async_session(session)
            self.assertEqual(session_, session)

    async def test_setup_async_session(self):
        async with _functions.setup_async_session(None) as session:
            self.assertIsInstance(session, httpx.AsyncClient)

    async def test_async_session_closer(self):
        async with httpx.AsyncClient() as session:
            await _functions.async_session_closer(session)
            self.assertTrue(session.is_closed)


if __name__ == "__main__":
    unittest.main()
