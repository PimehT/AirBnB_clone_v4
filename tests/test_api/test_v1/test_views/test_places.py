#!/usr/bin/python3
"""Test the api/v1/views/places.py module."""
import unittest
import os
import pycodestyle
from tests.test_api.test_v1.base_test import BaseTestCase, TestData
from api.v1.views import places
from models.place import Place
import json


class TestPlaceDocs(unittest.TestCase):
    """Checks that the documentation and style of places.py."""

    def test_pep8_conformance_places(self):
        """Test that api/v1/views/places.py conforms to PEP8."""
        pep8s = pycodestyle.StyleGuide(quiet=True)
        result = pep8s.check_files(['api/v1/views/places.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_places_module_docstring(self):
        """Test for the api/v1/views/places.py module docstring"""
        self.assertIsNot(places.__doc__, None,
                         "api/v1/views/places.py needs a docstring")
        self.assertTrue(len(places.__doc__) >= 1,
                        "api/v1/views/places.py needs a docstring")


class TestPlace(BaseTestCase):
    """Test the places module."""

    def setUp(self):
        """Create city obj which will have city."""
        super().setUp()
        self.test_data = TestData(self.storage)
        self.city = self.test_data.get('City')[0]
        self.place = self.test_data.get('Place')[0]
        self.user = self.test_data.get('User')[0]

    def tearDown(self):
        """Destroy test_data."""
        super().tearDown()
        del self.test_data
        del self.city
        del self.place
        del self.user

    def test_get_places(self):
        """Test route '/api/v1/cities/<city_id>/places'."""
        test_place_ids = [p.id for p in self.city.places]
        resp = self.client.get(f'/api/v1/cities/{self.city.id}/places')
        if resp.status_code != 200:
            return
        resp_place_ids = [d['id'] for d in resp.json]
        self.assertCountEqual(resp_place_ids, test_place_ids)

    def test_get_place_by_id_success(self):
        """Test success of route '/places/<place_id>'."""
        resp = self.client.get(f"/api/v1/places/{self.place.id}")
        self.assertEqual(resp.status_code, 200)

    def test_get_place_by_id_not_linked(self):
        """Test fail of route '/places/<place_id>'."""
        resp = self.client.get("/api/v1/places/000")
        self.assertEqual(resp.status_code, 404)

    def test_delete_place_success(self):
        """Test success delete place route."""
        resp = self.client.delete(f"/api/v1/places/{self.place.id}")
        self.assertEqual(len(resp.json), 0,
                         msg="Response.json should be an empty dictionary")
        self.assertIn(resp.status_code, [200, 204],
                      msg="Should return status code 200 or 204")

        resp2 = self.client.get(f"/api/v1/places/{self.place.id}")
        self.assertTrue(resp2.status_code, 404)

    def test_delete_place_fail(self):
        """Test fail delete place route."""
        resp = self.client.delete("/api/v1/places/000")
        self.assertTrue(resp.status_code, 404)

    def test_post_place_success(self):
        """Test success post place route."""
        headers = {"Content-Type": "application/json"}
        data = {
            "name": "Going Merry",
            "user_id": self.user.id
        }
        resp = self.client.post(f'/api/v1/cities/{self.city.id}/places',
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
        if "name" not in resp.json:
            self.fail("name key not in response.json")
            return
        self.assertEqual(resp.json["name"], data["name"],
                         msg=f'name != {data["name"]}')
        if "user_id" not in resp.json:
            self.fail("user_id key not in response.json")
            return
        self.assertEqual(resp.json["user_id"], data["user_id"],
                         msg=f'user_id != {data["user_id"]}')

    def test_post_place_fail_not_a_json(self):
        """Test that when HTTP body request is not valid JSON, return 400"""
        headers = {"Content-Type": "application/json"}
        resp = self.client.post(f'/api/v1/cities/{self.city.id}/places',
                                headers=headers, data=None)
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json, {'error': "Not a JSON"},
                         msg='Response.json is not {"error": "Not a JSON"}')

    def test_post_place_fail_does_not_contain_name(self):
        """Test that when dictionary doesnt contain key name, raise a 400"""
        headers = {"Content-Type": "application/json"}
        data = {
            "not_name": "Random name",
            "user_id": self.user.id
        }
        resp = self.client.post(f'/api/v1/cities/{self.city.id}/places',
                                headers=headers,
                                data=json.dumps(data))
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json, {'error': "Missing name"},
                         msg='Response.json is not {"error": "Missing name"}')

    def test_post_place_fail_does_not_contain_a_user_id(self):
        """Test that when dictionary doesnt contain key user_id, raise a 400"""
        headers = {"Content-Type": "application/json"}
        data = {
            "name": "Random name",
            "not_user_id": self.user.id
        }
        resp = self.client.post(f'/api/v1/cities/{self.city.id}/places',
                                headers=headers,
                                data=json.dumps(data))
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json, {'error': "Missing user_id"},
                         msg='Response.json is not {"error": "Missing user_id"}')

    def test_put_place_success(self):
        """Test put place success."""
        headers = {"Content-Type": "application/json"}
        data = {"name": "Going Merry is so cool"}
        resp = self.client.put(f'/api/v1/places/{self.place.id}',
                               headers=headers,
                               data=json.dumps(data))

        self.assertEqual(resp.status_code, 200,
                         msg="response.status_code != 200")

        if not resp.json or resp.json.get("name") is None:
            return
        self.assertEqual(resp.json["name"], "Going Merry is so cool",
                         msg="attr 'name' was not updated")

    def test_put_place_fail_not_a_json(self):
        """Test that when HTTP body request is not valid JSON, raise 400"""
        headers = {"Content-Type": "application/json"}
        resp = self.client.put(f'/api/v1/places/{self.place.id}',
                               headers=headers, data=None)
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json, {'error': "Not a JSON"},
                         msg='Response.json is not {"error": "Not a JSON"}')

    def test_put_place_ignore_keys(self):
        """
        Test put place ignores:
            id, user_id, city_id, created_at and updated_at
        """
        headers = {"Content-Type": "application/json"}
        data = {
            "id": "1a9c29c7-e39c-4840-b5f9-74310b34f269",
            "user_id": "1a9c29c7-e39c-4840-b5f9-74310b34f269",
            "city_id": "1a9c29c7-e39c-4840-b5f9-74310b34f269",
            "created_at": "2017-04-14T16:21:42",
            "updated_at": "2017-04-14T16:21:42"
        }
        resp = self.client.put(f'/api/v1/places/{self.place.id}',
                               headers=headers, data=json.dumps(data))

        self.assertEqual(resp.status_code, 200,
                         msg="status code should be 200 regardless")
        for k, v in data.items():
            with self.subTest(k=k, v=v):
                self.assertNotEqual(resp.json[k], v,
                                    msg=f"key {k} should not be updated")
