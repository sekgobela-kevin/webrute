from webrute import _attributes
from webrute import exceptions

import unittest


class SampleAttribute(_attributes.Attributes):
    _supported_attrs = set(("name", "age", "address"))
    _unsupported_attrs = set(("address", "race"))


class AttributesTest(unittest.TestCase):
    _attribute_type = _attributes.Attributes
    
    def setUp(self) -> None:
        self.setup_attributes_dict()
        # Get supported and unsupported attributes names
        self._unsupported_attrs_names = self._attribute_type._unsupported_attrs
        self._supported_attrs_names = self._attribute_type._supported_attrs

        # Retrieves attributes that are fully supported
        supported_attrs_names = self._supported_attrs_names or set()
        self._fully_supported_attrs_names = supported_attrs_names.difference(
            self._unsupported_attrs_names
        )

        # Tries to get first single fully supported attribute name
        if self._fully_supported_attrs_names:
            self._fully_supported_attr_name =\
                list(self._fully_supported_attrs_names)[0]
        else:
            self._fully_supported_attr_name = None

        # Tries to get first attribute name to use with attribute type.
        if self._attributes_dict:
            self._first_attr_name = list(self._attributes_dict.keys())[0]
        else:
            self._first_attr_name = None
        self._attribute = self._attribute_type(**self._attributes_dict)

    def setup_attributes_dict(self):
        self._attributes_dict = {"name": "John", "age":25}

    def test_get_attr(self):
        if self._attributes_dict:
            dict_key = self._first_attr_name
            attr_name = self._attribute.get_attr(dict_key)
            self.assertEqual(attr_name, self._attributes_dict[dict_key])
        self.assertEqual(self._attribute.get_attr("s s ses"), None)

    def test_get_attrs(self):
        self.assertDictEqual(self._attribute.get_attrs(), self._attributes_dict)

    def test_get_attrs_keys(self):
        self.assertListEqual(list(self._attribute.get_attrs_keys()), 
        list(self._attributes_dict.keys()))

    def get_attrs_values(self):
        self.assertListEqual(self._attribute.get_attrs_values(), 
        self._attributes_dict.values())

    def test_attr_exists(self):
        if self._attributes_dict:
            self.assertTrue(self._attribute.attr_exists(self._first_attr_name))
        self.assertFalse(self._attribute.attr_exists("ssdffd"))

    def test_attr_supported(self):
        # Any attribute name is supported if supported attributes and 
        # unsupported attributes are not provided.
        if self._supported_attrs_names is None and \
            not len(self._unsupported_attrs_names):
            self.assertTrue(self._attribute.attr_supported("ssdffd"))
        else:
            # 'ssdffd' is not supported attribute name.
            self.assertFalse(self._attribute.attr_supported("ssdffd"))
        # self._fully_supported_attr_name is supported if not None.
        if self._fully_supported_attr_name is not None:
            self.assertTrue(self._attribute.attr_supported(
                self._fully_supported_attr_name
            ))
        

    def test_attrs_supported(self):
        # See test_attr_supported() above.
        if self._supported_attrs_names is None and \
            not len(self._unsupported_attrs_names):
            # Any attribute is supported.
            self.assertTrue(self._attribute.attrs_supported(["ssdffd", "346"]))
        else:
            # Both 'ssdffd' and '346' are never supported.
            self.assertFalse(self._attribute.attrs_supported(["ssdffd", "346"]))
        # Atleast 0% of attributes names are supported.
        self.assertTrue(self._attribute.attrs_supported(["ssdffd", "346"], 0))
        # self._fully_supported_attrs_names is always supported.
        self.assertTrue(self._attribute.attrs_supported(
            self._fully_supported_attrs_names
        ))
        

    def test_get_supported_attrs(self):
        supported_attrs = self._supported_attrs_names or set()
        self.assertEqual(self._attribute.get_supported_attrs(), supported_attrs)

    def test_get_unsupported_attrs(self):
        unsupported_attrs = self._attribute.get_unsupported_attrs()
        self.assertEqual(self._attribute.get_unsupported_attrs(), 
            unsupported_attrs)

    def test_raise_for_unsupported(self):
        self._attribute.raise_for_unsupported(self._fully_supported_attrs_names)
        if self._supported_attrs_names is not None:
            with self.assertRaises(exceptions.UnsupportedAttribute):
                self._attribute.raise_for_unsupported(["ssdffd", "346"])

    def test_to_dict(self):
        self.assertDictEqual(self._attribute.to_dict(), self._attributes_dict)

    def test_to_instance(self):
        self.assertIsInstance(self._attribute.to_instance({}), 
            self._attribute_type)


class TestSampleAttribute(AttributesTest):
    _attribute_type = SampleAttribute



if __name__ == "__main__":
    unittest.main()
