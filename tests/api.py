# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import unittest
try:
    from unittest import mock
except ImportError:
    import mock

from requests.structures import CaseInsensitiveDict

from gyazo.api import Api
from gyazo.error import GyazoError


class TestApi(unittest.TestCase):
    def setUp(self):
        self.api = Api()

    def test_parse_and_check_success(self):
        mock_response = mock.MagicMock()
        headers = CaseInsensitiveDict()
        headers["X-Runtime"] = "0.008495"
        mock_response.headers = headers
        data = {
            "height": 320,
            "provider_name": "Gyazo",
            "provider_url": "https://gyazo.com",
            "type": "photo",
            "url": "https://bot.gyazo.com/e72675b15a56b1.png",
            "version": "1.0",
            "width": 640
        }
        mock_response.json.return_value = data
        mock_response.status_code = 200

        actual_headers, actual_data = self.api._parse_and_check(mock_response)

        self.assertEqual(actual_headers, headers)
        self.assertDictEqual(actual_data, data)

    def test_parse_and_check_error_exception(self):
        mock_response = mock.MagicMock()
        headers = CaseInsensitiveDict()
        headers["X-Runtime"] = "0.008495"
        mock_response.headers = headers
        mock_response.json.side_effect = ValueError
        mock_response.status_code = 200

        with self.assertRaises(ValueError):
            self.api._parse_and_check(mock_response)

    def test_parse_and_check_error_status_code(self):
        mock_response = mock.MagicMock()
        headers = CaseInsensitiveDict()
        headers["X-Runtime"] = "0.008495"
        mock_response.headers = headers
        data = {
            "message": "image not found."
        }
        mock_response.json.return_value = data
        mock_response.status_code = 404

        with self.assertRaises(GyazoError):
            self.api._parse_and_check(mock_response)

    def test_parse_and_check_error_status_code_without_message(self):
        mock_response = mock.MagicMock()
        headers = CaseInsensitiveDict()
        headers["X-Runtime"] = "0.008495"
        mock_response.headers = headers
        data = {}
        mock_response.json.return_value = data
        mock_response.status_code = 404

        with self.assertRaises(GyazoError):
            self.api._parse_and_check(mock_response)
