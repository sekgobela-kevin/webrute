from webrute import _util
import unittest


class foo():
    @staticmethod
    def static_method(cls, name, address): pass
    def method(self, name, address): pass

def function(name, address): pass

class Test(unittest.TestCase):
    def test_extract_arguments(self):
        arguments = ["name", "address"]
        method_arguments = ["self"] + arguments
        static_arguments = ["cls"] + arguments
        self.assertEqual(_util.extract_arguments(function), arguments)
        self.assertEqual(_util.extract_arguments(foo.method), method_arguments)
        self.assertEqual(_util.extract_arguments(foo.static_method), static_arguments)

        self.assertEqual(_util.extract_arguments(foo.method, True), arguments)
        self.assertEqual(_util.extract_arguments(foo.static_method, True), arguments)

    def test_has_implicit_argument(self):
        self.assertFalse(_util.has_implicit_argument(function))
        self.assertTrue(_util.has_implicit_argument(foo.method))
        self.assertTrue(_util.has_implicit_argument(foo.static_method))



if __name__ == "__main__":
    unittest.main()
