from webrute import _highlevel
import webrute
import unittest


class Test(unittest.TestCase):
    def setUp(self) -> None:
        self._table = webrute.table([webrute.field("", [])])
        self._string_target = "https://example.com/"
        self._dict_target = {"url": "https://example.com/"}
        self._runner_args = {
            "table": self._table,
            "optimize": False
        }

        self._normal_runner_args = {
            **self._runner_args,
            "success": lambda r: False,
            "failure": lambda r: True,
            "max_success_records":10000
        }

        async def success(r): return False
        async def failure(r): return True

        self._async_runner_args = {
            **self._runner_args,
            "success": success,
            "failure": failure
        }
    
    def test_create_runner(self):
        _runner = _highlevel.create_runner(self._string_target, 
            **self._normal_runner_args)
        _runner = _highlevel.create_runner(self._dict_target, 
            **self._normal_runner_args)
        self.assertIsInstance(_runner, webrute.runner)

    def test_create_runner(self):
        _runner = _highlevel.create_basic_runner(self._string_target, 
            **self._normal_runner_args)
        self.assertIsInstance(_runner, webrute.basic_runner)

    def test_create_runner(self):
        _runner = _highlevel.create_thread_runner(self._string_target, 
            **self._normal_runner_args)
        self.assertIsInstance(_runner, webrute.thread_runner)

    def test_create_runner(self):
        _runner = _highlevel.create_async_runner(self._string_target, 
            **self._async_runner_args)
        self.assertIsInstance(_runner, webrute.async_runner)



if __name__ == "__main__":
    unittest.main()

