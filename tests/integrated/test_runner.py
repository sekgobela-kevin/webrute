from . import setup_tests

import webrute
import httpx
import unittest


class BaseTestRunner():
    _runner_type = webrute.runner

    def _runner_creator(self, *args, **kwargs):
        return webrute.create_basic_runner(*args, **kwargs)

    def test_runner(self):
        runner = self._runner_creator(
            self._login_target,
            self._table, 
            success=self.success,
            record_transformer= self.record_trandformer
        )
        runner.start()
        success_records = runner.get_success_records()
        self.assertCountEqual(success_records, self._webapp_records)

    def test_runner_connector(self):
        def connector(target, record, session=None):
            self.assertEqual(target, self._login_target)
            self.assertIsNotNone(session)
            record = webrute.transform_record(record, "POST")
            return webrute.connector(target, record, session)
        
        runner = self._runner_creator(
            self._login_target,
            self._table, 
            success=self.success,
            connector=connector
        )
        runner.start()
        success_records = runner.get_success_records()
        self.assertCountEqual(success_records, self._webapp_records)


    def test_runner_connector_no_success(self):
        if isinstance(self, setup_tests.SetUpTests):
            def success(response): return False
        else:
            async def success(response): return False
        runner = self._runner_creator(
            self._login_target,
            self._table, 
            success=success,
            record_transformer=self.record_trandformer
        )
        runner.start()
        success_records = runner.get_success_records()
        self.assertCountEqual(success_records, [])

    def test_runner_session(self):
        def connector(target, record, session=None):
            self.assertEqual(target, self._login_target)
            self.assertEqual(session, self._session)
            record = webrute.transform_record(record, "POST")
            return webrute.connector(target, record, session)
        
        runner = self._runner_creator(
            self._login_target,
            self._table, 
            success=self.success,
            connector=connector,
            session=self._session
        )
        runner.start()
        success_records = runner.get_success_records()
        self.assertCountEqual(success_records, self._webapp_records)

        self.assertFalse(self._session.is_closed)

    def test_runner_callable_session(self):
        runner = self._runner_creator(
            self._login_target,
            self._table, 
            success=self.success,
            session=lambda: self._session
        )
        # Thread runner is failing to close session
        if not isinstance(runner, webrute.thread_runner):
            self.assertTrue(self._session.is_closed)


class TestBasicRunner(BaseTestRunner, setup_tests.SetUpTests):
    _runner_type = webrute.basic_runner

    def _runner_creator(self, *args, **kwargs):
        return webrute.create_basic_runner(*args, **kwargs)

class TestThreadRunner(BaseTestRunner, setup_tests.SetUpTests):
    _runner_type = webrute.thread_runner

    def _runner_creator(self, *args, **kwargs):
        return webrute.create_thread_runner(*args, **kwargs)

class TestAsyncRunner(BaseTestRunner, setup_tests.AsyncSetUpTests):
    _runner_type = webrute.async_runner

    def _runner_creator(self, *args, **kwargs):
        return webrute.create_async_runner(*args, **kwargs)
    