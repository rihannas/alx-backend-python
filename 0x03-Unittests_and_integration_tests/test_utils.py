#!/usr/bin/env python3
"""Unittest for utils.access_nested_map"""

import unittest
from utils import access_nested_map

from parameterized import parameterized

""" Note: Parameterized tests allow a developer to run the same test over
and over again using different values. """


class TestAccessNestedMap(unittest.TestCase):
    """class that test the function access_nested_map"""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expexted_value):
        """tests access_nested_map function"""

        self.assertEqual(access_nested_map(nested_map, path), expexted_value)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b"))
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """ Uses the assertRaises context manager to test that a KeyError is raised."""
        self.assertRaises(KeyError, access_nested_map, nested_map, path)


if __name__ == '__main__':
    unittest.main()
