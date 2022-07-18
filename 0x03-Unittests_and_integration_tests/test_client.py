#!/usr/bin/env python3
"""Unit tests for client.py"""

import unittest
from unittest.mock import Mock, patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """class to test GithubOrgClient class"""

    @parameterized.expand([
        ("google"),
        ("abc")
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_json):
        """
        test that GithubOrgClient.org returns correct value.
        """
        test_class = GithubOrgClient(org_name)
        test_class.org()
        mock_json.assert_called_once_with(
            'https://api.github.com/orgs/{}'.format(org_name))
