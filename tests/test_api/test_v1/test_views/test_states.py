#!/usr/bin/python3
"""Test the api/v1/views/states.py module."""
import unittest
import os
import pycodestyle
from tests.test_api.test_v1.base_test import BaseTestCase, TestData
from api.v1.views import states
from models.state import State
import json


class TestStateDocs(unittest.TestCase):
    """Checks that the documentation and style of states.py."""

    def test_pep8_conformance_states(self):
        """Test that api/v1/views/states.py conforms to PEP8."""
        pep8s = pycodestyle.StyleGuide(quiet=True)
        result = pep8s.check_files(['api/v1/views/states.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_states_module_docstring(self):
        """Test for the api/v1/views/states.py module docstring"""
        self.assertIsNot(states.__doc__, None,
                         "api/v1/views/states.py needs a docstring")
        self.assertTrue(len(states.__doc__) >= 1,
                        "api/v1/views/states.py needs a docstring")


class TestState(BaseTestCase):
    """Test the states module."""

    def test_get_states(self):
        """Test route '/states'."""
        test_data = TestData(self.storage)
        test_state_ids = [state.id for state in test_data.get('State')]
        resp = self.client.get('/api/v1/states/')
        if resp.status_code != 200:
            return
        resp_state_ids = [d['id'] for d in resp.json]
        self.assertCountEqual(resp_state_ids, test_state_ids)

    def test_get_state_by_id_success(self):
        """Test success of route '/states/<state_id>'."""
        test_data = TestData(self.storage)
        test_state_id = test_data.get('State')[0].id
        resp = self.client.get(f"/api/v1/states/{test_state_id}")
        self.assertEqual(resp.status_code, 200)

    def test_get_state_by_id_not_linked(self):
        """Test fail of route '/states/<state_id>'."""
        resp = self.client.get("/api/v1/states/000")
        self.assertEqual(resp.status_code, 404)

    def test_delete_state_success(self):
        """Test success delete state route."""
        test_data = TestData(self.storage)
        test_state_id = test_data.get('State')[0].id

        resp = self.client.delete(f"/api/v1/states/{test_state_id}")
        self.assertEqual(len(resp.json), 0,
                         msg="Response.json should be an empty dictionary")
        self.assertIn(resp.status_code, [200, 204],
                      msg="Should return status code 200 or 204")

        resp2 = self.client.get(f"/api/v1/states/{test_state_id}")
        self.assertTrue(resp2.status_code, 404)

    def test_delete_state_fail(self):
        """Test fail delete state route."""
        resp = self.client.delete("/api/v1/states/000")
        self.assertTrue(resp.status_code, 404)

    def test_post_state_success(self):
        """Test success post state route."""
        headers = {"Content-Type": "application/json"}
        data = {"name": "California"}
        resp = self.client.post('/api/v1/states/', headers=headers,
                                data=json.dumps(data))
        self.assertEqual(resp.status_code, 201,
                         msg="Should return status code 201")
        if len(resp.json) == 0:
            self.fail("Response.json should not be length 0")
            return
        self.assertIn("id", resp.json,
                      msg="id key not in response.json")
        self.assertIn("created_at", resp.json,
                      msg="created_at key not in response.json")
        self.assertIn("updated_at", resp.json,
                      msg="updated_at key not in response.json")
        if "name" not in resp.json:
            self.fail("name key not in response.json")
            return
        self.assertEqual(resp.json["name"], "California",
                         msg="name != California")

    def test_post_state_fail_not_a_json(self):
        """Test that when HTTP body request is not valid JSON, return 400"""
        headers = {"Content-Type": "application/json"}
        resp = self.client.post('/api/v1/states/', headers=headers, data=None)
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json, {'error': "Not a JSON"},
                         msg='Response.json is not {"error": "Not a JSON"}')

    def test_post_state_fail_does_not_contain_a_key(self):
        """Test that when dictionary doesnt contain key name, raise a 400"""
        headers = {"Content-Type": "application/json"}
        data = {"not_name": "California"}
        resp = self.client.post('/api/v1/states/', headers=headers,
                                data=json.dumps(data))
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json, {'error': "Missing name"},
                         msg='Response.json is not {"error": "Missing name"}')

    def test_put_state_success(self):
        """Test post state success."""
        test_data = TestData(self.storage)
        test_state = test_data.get('State')[0]
        headers = {"Content-Type": "application/json"}
        data = {"name": "California is so cool"}
        resp = self.client.put(f'/api/v1/states/{test_state.id}',
                               headers=headers,
                               data=json.dumps(data))

        self.assertEqual(resp.status_code, 200,
                         msg="response.status_code != 200")

        if not resp.json or resp.json.get("name") is None:
            return
        self.assertEqual(resp.json["name"], "California is so cool",
                         msg="attr 'name' was not updated")

    def test_put_state_fail_not_a_json(self):
        """Test that when HTTP body request is not valid JSON, raise 400"""
        test_data = TestData(self.storage)
        test_state = test_data.get('State')[0]
        headers = {"Content-Type": "application/json"}
        resp = self.client.put(f'/api/v1/states/{test_state.id}',
                               headers=headers, data=None)
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json, {'error': "Not a JSON"},
                         msg='Response.json is not {"error": "Not a JSON"}')

    def test_put_state_ignore_keys(self):
        """Test that put state ignores keys: id, created_at and updated_at"""
        test_data = TestData(self.storage)
        test_state = test_data.get('State')[0]
        headers = {"Content-Type": "application/json"}
        data = {
            "id": "1a9c29c7-e39c-4840-b5f9-74310b34f269",
            "created_at": "2017-04-14T16:21:42",
            "updated_at": "2017-04-14T16:21:42"
        }
        resp = self.client.put(f'/api/v1/states/{test_state.id}',
                               headers=headers, data=json.dumps(data))

        self.assertEqual(resp.status_code, 200,
                         msg="status code should be 200 regardless")
        self.assertNotEqual(resp.json['id'], data['id'],
                            msg="key 'id' should not be updated")
        self.assertNotEqual(resp.json['created_at'], data['created_at'],
                            msg="key 'created_at' should not be updated")
        self.assertNotEqual(resp.json['updated_at'], data['updated_at'],
                            msg="key 'updated_at' should not be updated")
