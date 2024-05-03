#!/usr/bin/python3
"""Test the api/v1/views/users.py module."""
import unittest
import os
import pycodestyle
from tests.test_api.test_v1.base_test import BaseTestCase, TestData
from api.v1.views import users
from models.user import User
import json


class TestUserDocs(unittest.TestCase):
    """Checks that the documentation and style of users.py."""

    def test_pep8_conformance_user(self):
        """Test that api/v1/views/users.py conforms to PEP8."""
        pep8s = pycodestyle.StyleGuide(quiet=True)
        result = pep8s.check_files(['api/v1/views/users.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_users_module_docstring(self):
        """Test for the api/v1/views/users.py module docstring"""
        self.assertIsNot(users.__doc__, None,
                         "api/v1/views/users.py needs a docstring")
        self.assertTrue(len(users.__doc__) >= 1,
                        "api/v1/views/users.py needs a docstring")


class TestUser(BaseTestCase):
    """Test the users module."""

    def setUp(self):
        """Create user obj"""
        super().setUp()
        self.test_data = TestData(self.storage)
        self.user = self.test_data.get('User')[0]

    def tearDown(self):
        """Destroy test_data."""
        try:
            del self.test_data
            del self.user
        except AttributeError:
            pass
        super().tearDown()

    def test_get_users(self):
        """Test route '/users'."""
        test_user_ids = [a.id for a in self.test_data.get('User')]
        resp = self.client.get('/api/v1/users')
        if resp.status_code != 200:
            return
        resp_user_ids = [d['id'] for d in resp.json]
        self.assertCountEqual(resp_user_ids, test_user_ids)

    def test_get_user_by_id_success(self):
        """Test success of route '/users/<user_id>'."""
        resp = self.client.get(f"/api/v1/users/{self.user.id}")
        self.assertEqual(resp.status_code, 200)

    def test_get_user_by_id_not_linked(self):
        """Test fail of route '/users/<user_id>'."""
        resp = self.client.get("/api/v1/users/000")
        self.assertEqual(resp.status_code, 404)

    def test_delete_user_success(self):
        """Test success delete user route."""
        resp = self.client.delete(f"/api/v1/users/{self.user.id}")
        self.assertEqual(len(resp.json), 0,
                         msg="Response.json should be an empty dictionary")
        self.assertIn(resp.status_code, [200, 204],
                      msg="Should return status code 200 or 204")

        resp2 = self.client.get(f"/api/v1/users/{self.user.id}")
        self.assertTrue(resp2.status_code, 404)

    def test_delete_user_fail(self):
        """Test fail delete user route."""
        resp = self.client.delete("/api/v1/users/000")
        self.assertTrue(resp.status_code, 404)

    def test_post_user_success(self):
        """Test success post user route."""
        headers = {"Content-Type": "application/json"}
        data = {
            "name": "User1",
            "email": "user1@gmail.com",
            "password": "weakpassword"
        }
        resp = self.client.post('/api/v1/users/',
                                headers=headers,
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
        for key, value in data.items():
            with self.subTest(key=key, value=value):
                if key not in resp.json:
                    self.fail(f"{key} key not in response.json")
                continue
                self.assertEqual(resp.json[key], value,
                                 msg=f"{key} != {value}")

    def test_post_user_fail_not_a_json(self):
        """Test that when HTTP body request is not valid JSON, return 400"""
        headers = {"Content-Type": "application/json"}
        resp = self.client.post('/api/v1/users/',
                                headers=headers, data=None)
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json, {'error': "Not a JSON"},
                         msg='Response.json is not {"error": "Not a JSON"}')

    def test_post_user_fail_missing_email(self):
        """Test that when dictionary doesnt contain key email, raise a 400"""
        headers = {"Content-Type": "application/json"}
        data = {
            "name": "User1",
            "password": "weakpassword",
            "not_email": "Random email"
        }
        resp = self.client.post(f'/api/v1/users',
                                headers=headers,
                                data=json.dumps(data))
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json, {'error': "Missing email"},
                         msg='Response.json not {"error": "Missing email"}')

    def test_post_user_fail_missing_password(self):
        """Test when dictionary doesnt contain key password, raise a 400"""
        headers = {"Content-Type": "application/json"}
        data = {
            "name": "User1",
            "not_password": "weakpassword",
            "email": "Random email"
        }
        resp = self.client.post(f'/api/v1/users',
                                headers=headers,
                                data=json.dumps(data))
        self.assertEqual(resp.status_code, 400)
        msg = 'Response.json not {"error": "Missing password"}'
        self.assertEqual(resp.json, {'error': "Missing password"}, msg=msg)

    def test_put_user_success(self):
        """Test post city success."""
        headers = {"Content-Type": "application/json"}
        data = {"name": "User1 is so cool"}
        resp = self.client.put(f'/api/v1/users/{self.user.id}',
                               headers=headers,
                               data=json.dumps(data))

        self.assertEqual(resp.status_code, 200,
                         msg="response.status_code != 200")

        if not resp.json or resp.json.get("name") is None:
            return
        self.assertEqual(resp.json["name"], "User1 is so cool",
                         msg="attr 'name' was not updated")

    def test_put_user_fail_not_a_json(self):
        """Test that when HTTP body request is not valid JSON, raise 400"""
        headers = {"Content-Type": "application/json"}
        resp = self.client.put(f'/api/v1/users/{self.user.id}',
                               headers=headers, data=None)
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json, {'error': "Not a JSON"},
                         msg='Response.json is not {"error": "Not a JSON"}')

    def test_put_user_ignore_keys(self):
        """Test put city ignores: id, email, created_at and updated_at"""
        headers = {"Content-Type": "application/json"}
        data = {
            "id": "1a9c29c7-e39c-4840-b5f9-74310b34f269",
            "created_at": "2017-04-14T16:21:42",
            "updated_at": "2017-04-14T16:21:42",
            "email": "hacker@gmail.com"
        }
        resp = self.client.put(f'/api/v1/users/{self.user.id}',
                               headers=headers, data=json.dumps(data))

        self.assertEqual(resp.status_code, 200,
                         msg="status code should be 200 regardless")
        self.assertNotEqual(resp.json['id'], data['id'],
                            msg="key 'id' should not be updated")
        self.assertNotEqual(resp.json['created_at'], data['created_at'],
                            msg="key 'created_at' should not be updated")
        self.assertNotEqual(resp.json['updated_at'], data['updated_at'],
                            msg="key 'updated_at' should not be updated")
        self.assertNotEqual(resp.json['email'], data['email'],
                            msg="key 'email' should not be updated")
