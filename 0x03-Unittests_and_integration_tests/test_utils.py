#!/usr/bin/env python3
"""Unittest for utils.access_nested_map"""

import unittest
from unittest.mock import Mock, patch
from utils import access_nested_map, get_json

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
    def test_access_nested_map(self, nested_map, path, expected_value):
        """tests access_nested_map function expected value"""

        self.assertEqual(access_nested_map(nested_map, path), expected_value)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b"))
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """
        Uses the assertRaises context manager
        to test that a KeyError is raised.
        """
        self.assertRaises(KeyError, access_nested_map, nested_map, path)


class TestGetJson(unittest.TestCase):
    """class test for get_json function"""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    def test_get_json(self, test_url, test_payload):
        """
        1. Tests that the mocked get method was called exactly once
        (per input) with test_url as argument.
        2. Test that the output of get_json is equal to test_payload.
        """
        # create Mock object with json method that returns test_payload
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        # function calls requests.get, need patch to get mock return value
        with patch('requests.get', return_value=mock_response):
            real_response = get_json(test_url)
            self.assertEqual(real_response, test_payload)
            # check that mocked method called once per input
            mock_response.json.assert_called_once()


if __name__ == '__main__':
    unittest.main()
