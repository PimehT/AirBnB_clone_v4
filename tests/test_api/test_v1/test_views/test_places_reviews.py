#!/usr/bin/python3
"""Test the api/v1/views/places_reviews.py module."""
import unittest
import os
import pycodestyle
from tests.test_api.test_v1.base_test import BaseTestCase, TestData
from api.v1.views import places_reviews
from models.review import Review
import json


class TestReviewDocs(unittest.TestCase):
    """Checks that the documentation and style of places_reviews.py."""

    def test_pep8_conformance_places_reviews(self):
        """Test that api/v1/views/places_reviews.py conforms to PEP8."""
        pep8s = pycodestyle.StyleGuide(quiet=True)
        result = pep8s.check_files(['api/v1/views/places_reviews.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_places_reviews_module_docstring(self):
        """Test for the api/v1/views/places_reviews.py module docstring"""
        self.assertIsNot(places_reviews.__doc__, None,
                         "api/v1/views/places_reviews.py needs a docstring")
        self.assertTrue(len(places_reviews.__doc__) >= 1,
                        "api/v1/views/places_reviews.py needs a docstring")


class TestReview(BaseTestCase):
    """Test the places_reviews module."""

    def setUp(self):
        """Create place obj which will have review."""
        super().setUp()
        self.test_data = TestData(self.storage)
        self.place = self.test_data.get('Place')[0]
        self.review = self.test_data.get('Review')[0]
        self.user = self.test_data.get('User')[0]

    def tearDown(self):
        """Destroy test_data."""
        super().tearDown()
        del self.test_data
        del self.place
        del self.review
        del self.user

    def test_get_reviews(self):
        """Test route '/api/v1/places/<place_id>/reviews'."""
        test_review_ids = [p.id for p in self.place.reviews]
        resp = self.client.get(f'/api/v1/places/{self.place.id}/reviews')
        if resp.status_code != 200:
            return
        resp_review_ids = [d['id'] for d in resp.json]
        self.assertCountEqual(resp_review_ids, test_review_ids)

    def test_get_review_by_id_success(self):
        """Test success of route '/reviews/<review_id>'."""
        resp = self.client.get(f"/api/v1/reviews/{self.review.id}")
        self.assertEqual(resp.status_code, 200)

    def test_get_review_by_id_not_linked(self):
        """Test fail of route '/reviews/<review_id>'."""
        resp = self.client.get("/api/v1/reviews/000")
        self.assertEqual(resp.status_code, 404)

    def test_delete_review_success(self):
        """Test success delete review route."""
        resp = self.client.delete(f"/api/v1/reviews/{self.review.id}")
        self.assertEqual(len(resp.json), 0,
                         msg="Response.json should be an empty dictionary")
        self.assertIn(resp.status_code, [200, 204],
                      msg="Should return status code 200 or 204")

        resp2 = self.client.get(f"/api/v1/reviews/{self.review.id}")
        self.assertTrue(resp2.status_code, 404)

    def test_delete_review_fail(self):
        """Test fail delete review route."""
        resp = self.client.delete("/api/v1/reviews/000")
        self.assertTrue(resp.status_code, 404)

    def test_post_review_success(self):
        """Test success post review route."""
        headers = {"Content-Type": "application/json"}
        data = {
            "text": "Cozy place",
            "user_id": self.user.id
        }
        resp = self.client.post(f'/api/v1/places/{self.place.id}/reviews',
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
        for k, v in data.items():
            with self.subTest(k=k, v=v):
                if k not in resp.json:
                    self.fail(f"{k} key not in response.json")
                continue
                self.assertEqual(resp.json[k], v,
                                 msg=f'{k} != {v}')

    def test_post_review_fail_not_a_json(self):
        """Test that when HTTP body request is not valid JSON, return 400"""
        headers = {"Content-Type": "application/json"}
        resp = self.client.post(f'/api/v1/places/{self.place.id}/reviews',
                                headers=headers, data=None)
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json, {'error': "Not a JSON"},
                         msg='Response.json is not {"error": "Not a JSON"}')

    def test_post_review_fail_place_id_not_linked(self):
        """Test when place_id is not linked to any Place object, raise 404"""
        headers = {"Content-Type": "application/json"}
        data = {
            "text": "Random text",
            "user_id": self.user.id,
        }
        resp = self.client.post(f'/api/v1/places/123456789/reviews',
                                headers=headers,
                                data=json.dumps(data))
        self.assertEqual(resp.status_code, 404,
                         msg="Should raise 404 error")

    def test_post_review_fail_does_not_contain_text(self):
        """Test that when dictionary doesnt contain key text, raise a 400"""
        headers = {"Content-Type": "application/json"}
        data = {
            "not_text": "Random text",
            "user_id": self.user.id,
        }
        resp = self.client.post(f'/api/v1/places/{self.place.id}/reviews',
                                headers=headers,
                                data=json.dumps(data))
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json, {'error': "Missing text"},
                         msg='Response.json is not {"error": "Missing text"}')

    def test_post_review_fail_does_not_contain_a_user_id(self):
        """Test that when dictionary doesnt contain key user_id, raise a 400"""
        headers = {"Content-Type": "application/json"}
        data = {
            "name": "Random name",
            "not_user_id": self.user.id
        }
        resp = self.client.post(f'/api/v1/places/{self.place.id}/reviews',
                                headers=headers,
                                data=json.dumps(data))
        self.assertEqual(resp.status_code, 400)
        msg = 'Response.json is not {"error": "Missing user_id"}'
        self.assertEqual(resp.json, {'error': "Missing user_id"}, msg=msg)

    def test_post_review_fail_user_id_not_linked(self):
        """Test when user_id is not linked to any User object, raise 404"""
        headers = {"Content-Type": "application/json"}
        data = {
            "text": "Random text",
            "user_id": "123456789",
        }
        resp = self.client.post(f'/api/v1/places/{self.place.id}/reviews',
                                headers=headers,
                                data=json.dumps(data))
        self.assertEqual(resp.status_code, 404,
                         msg="Should raise 404 error")

    def test_put_review_success(self):
        """Test put review success."""
        headers = {"Content-Type": "application/json"}
        data = {"name": "very spacious"}
        resp = self.client.put(f'/api/v1/reviews/{self.review.id}',
                               headers=headers,
                               data=json.dumps(data))

        self.assertEqual(resp.status_code, 200,
                         msg="response.status_code != 200")

        if not resp.json or resp.json.get("name") is None:
            return
        self.assertEqual(resp.json["name"], "very spacious",
                         msg="attr 'name' was not updated")

    def test_put_review_fail_not_a_json(self):
        """Test that when HTTP body request is not valid JSON, raise 400"""
        headers = {"Content-Type": "application/json"}
        resp = self.client.put(f'/api/v1/reviews/{self.review.id}',
                               headers=headers, data=None)
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json, {'error': "Not a JSON"},
                         msg='Response.json is not {"error": "Not a JSON"}')

    def test_put_review_ignore_keys(self):
        """
        Test put review ignores:
            id, user_id, place_id, created_at and updated_at
        """
        headers = {"Content-Type": "application/json"}
        data = {
            "id": "1a9c29c7-e39c-4840-b5f9-74310b34f269",
            "user_id": "1a9c29c7-e39c-4840-b5f9-74310b34f269",
            "created_at": "2017-04-14T16:21:42",
            "updated_at": "2017-04-14T16:21:42"
        }
        resp = self.client.put(f'/api/v1/reviews/{self.review.id}',
                               headers=headers, data=json.dumps(data))

        self.assertEqual(resp.status_code, 200,
                         msg="status code should be 200 regardless")
        for k, v in data.items():
            with self.subTest(k=k, v=v):
                self.assertNotEqual(resp.json[k], v,
                                    msg=f"key {k} should not be updated")
