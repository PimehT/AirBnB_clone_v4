#!/usr/bin/python3
"""Test the api/v1/views/index.py module."""
import unittest
import os
import pycodestyle
from tests.test_api.test_v1.base_test import BaseTestCase, TestData
from api.v1.views import index

class TestIndexDocs(unittest.TestCase):
    """Checks that the documentation and style of index.py."""

    def test_pep8_conformance_index(self):
        """Test that api/v1/views/index.py conforms to PEP8."""
        pep8s = pycodestyle.StyleGuide(quiet=True)
        result = pep8s.check_files(['api/v1/views/index.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_index_module_docstring(self):
        """Test for the api/v1/views/index.py module docstring"""
        self.assertIsNot(index.__doc__, None,
                         "api/v1/views/index.py needs a docstring")
        self.assertTrue(len(index.__doc__) >= 1,
                        "api/v1/views/index.py needs a docstring")


class TestIndex(BaseTestCase):
    """Test the index module."""

    def test_get_status(self):
        """Ensure that status returns ok."""
        resp = self.client.get('/api/v1/status')
        self.assertEqual(resp.json, {"status": "OK"})
        self.assertEqual(resp.status_code, 200)

    def test_get_stats(self):
        """Test output of stats."""
        test_obj = TestData(self.storage)
        resp = self.client.get('/api/v1/stats')
        self.assertEqual(resp.json, test_obj.counter)
