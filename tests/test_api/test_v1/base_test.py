#!/usr/bin/python3
"""Base test case from which other tests shall inherit."""
import os
import unittest

os.environ['HBNB_ENV'] = 'test'

from models.engine.file_storage import FileStorage
from api.v1 import app as app_py
from models import storage, TEST_PATH
from models.engine.file_storage import FileStorage
from models.base_model import Base
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.user import User
from datetime import datetime
import uuid
from collections import Counter
import inspect


class BaseTestCase(unittest.TestCase):
    """Base class for all tests."""

    @classmethod
    def setUpClass(cls):
        """
        set up
        """
        cls.storage = storage


    def setUp(self):
        """
        Create client.
        """
        app_py.app.config['TESTING'] = True
        self.client = app_py.app.test_client()

        # reload data from database/file.json
        self.storage.reload()
        if os.getenv('HBNB_TYPE_STORAGE') == 'db':
            self.session = self.storage._DBStorage__session
            self.objects = {}
        else:
            self.session = None
            self.objects = self.storage.all()

    def tearDown(self):
        """Post clean up"""
        # clear the database
        if os.getenv('HBNB_TYPE_STORAGE') == 'db':
            Base.metadata.drop_all(self.storage._DBStorage__engine)
        else:
            self.storage._FileStorage__objects = {}

        # clear the file.json
        if os.path.isfile(TEST_PATH):
            os.remove(TEST_PATH)
        

class TestData:
    """Class to create and describe test data."""

    def __init__(self, storage_obj):
        # clear TEST_PATH
        if os.path.isfile(TEST_PATH):
            os.remove(TEST_PATH)

        s1 = State(id=str(uuid.uuid4()), created_at=datetime.utcnow(),
                   updated_at=datetime.utcnow(), name="State_1")
        s2 = State(id=str(uuid.uuid4()), created_at=datetime.utcnow(),
                   updated_at=datetime.utcnow(), name="State_2")

        u1 = User(id=str(uuid.uuid4()), created_at=datetime.utcnow(),
                  updated_at=datetime.utcnow(), email="user1@gmail.com",
                  password="weakpassword1")
        u2 = User(id=str(uuid.uuid4()), created_at=datetime.utcnow(),
                  updated_at=datetime.utcnow(), email="user2@gmail.com",
                  password="weakpassword2")
        u3 = User(id=str(uuid.uuid4()), created_at=datetime.utcnow(),
                  updated_at=datetime.utcnow(), email="user3@gmail.com",
                  password="weakpassword3")

        c1 = City(id=str(uuid.uuid4()), created_at=datetime.utcnow(),
                  updated_at=datetime.utcnow(), name="City_1", state_id=s1.id)
        c2 = City(id=str(uuid.uuid4()), created_at=datetime.utcnow(),
                  updated_at=datetime.utcnow(), name="City_2", state_id=s1.id)
        c3 = City(id=str(uuid.uuid4()), created_at=datetime.utcnow(),
                  updated_at=datetime.utcnow(), name="City_3", state_id=s2.id)

        a1 = Amenity(id=str(uuid.uuid4()), created_at=datetime.utcnow(),
                     updated_at=datetime.utcnow(), name="amenity_1")
        a2 = Amenity(id=str(uuid.uuid4()), created_at=datetime.utcnow(),
                     updated_at=datetime.utcnow(), name="amenity_2")
        a3 = Amenity(id=str(uuid.uuid4()), created_at=datetime.utcnow(),
                     updated_at=datetime.utcnow(), name="amenity_3")
        a4 = Amenity(id=str(uuid.uuid4()), created_at=datetime.utcnow(),
                     updated_at=datetime.utcnow(), name="amenity_4")
        a5 = Amenity(id=str(uuid.uuid4()), created_at=datetime.utcnow(),
                     updated_at=datetime.utcnow(), name="amenity_5")

        p1 = Place(id=str(uuid.uuid4()), created_at=datetime.utcnow(),
                   city_id=c1.id, user_id=u3.id,
                   updated_at=datetime.utcnow(), name="place_1",
                   number_rooms=1, number_bathrooms=1, max_guest=1,
                   price_by_night=100, latitude=1.0, longitude=1.0)
        p2 = Place(id=str(uuid.uuid4()), created_at=datetime.utcnow(),
                   city_id=c1.id, user_id=u3.id,
                   updated_at=datetime.utcnow(), name="place_2",
                   number_rooms=2, number_bathrooms=2, max_guest=2,
                   price_by_night=200, latitude=2.0, longitude=2.0)
        p3 = Place(id=str(uuid.uuid4()), created_at=datetime.utcnow(),
                   city_id=c1.id, user_id=u3.id,
                   updated_at=datetime.utcnow(), name="place_3",
                   number_rooms=3, number_bathrooms=3, max_guest=3,
                   price_by_night=300, latitude=3.0, longitude=3.0)
        p4 = Place(id=str(uuid.uuid4()), created_at=datetime.utcnow(),
                   city_id=c1.id, user_id=u3.id,
                   updated_at=datetime.utcnow(), name="place_4",
                   number_rooms=4, number_bathrooms=4, max_guest=4,
                   price_by_night=400, latitude=4.0, longitude=4.0)
        p5 = Place(id=str(uuid.uuid4()), created_at=datetime.utcnow(),
                   city_id=c2.id, user_id=u3.id,
                   updated_at=datetime.utcnow(), name="place_5",
                   number_rooms=5, number_bathrooms=5, max_guest=5,
                   price_by_night=500, latitude=5.0, longitude=5.0)
        p6 = Place(id=str(uuid.uuid4()), created_at=datetime.utcnow(),
                   city_id=c3.id, user_id=u3.id,
                   updated_at=datetime.utcnow(), name="place_6",
                   number_rooms=6, number_bathrooms=6, max_guest=6,
                   price_by_night=600, latitude=6.0, longitude=6.0)

        r1 = Review(id=str(uuid.uuid4()), created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(), place_id=p1.id,
                    user_id=u1.id, text="review_1")
        r2 = Review(id=str(uuid.uuid4()), created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(), place_id=p2.id,
                    user_id=u1.id, text="review_2")
        r3 = Review(id=str(uuid.uuid4()), created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(), place_id=p3.id,
                    user_id=u1.id, text="review_3")
        r4 = Review(id=str(uuid.uuid4()), created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(), place_id=p4.id,
                    user_id=u2.id, text="review_4")
        r5 = Review(id=str(uuid.uuid4()), created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(), place_id=p5.id,
                    user_id=u2.id, text="review_5")
        
        self.objects = (
            s1, s2, u1, u2, u3, c1, c2, c3, a1, a2, a3, a4, a5, p1, p2,
            p3, p4, p5, p6, r1, r2, r3, r4, r5
        )

        self.save_objects(self.objects, storage_obj)

        obj_map = dict()
        for k, v in locals().items():
            if v in self.objects:
                obj_map[k] = v
        counter = dict()

        classes = {
            'Amenity': 'amenities',
            'City': 'cities',
            'Place': 'places',
            'Review': 'reviews',
            'State': 'states',
            'User': 'users',
        }

        for k, v in obj_map.items():
            cls_name = v.__class__.__name__
            cls = classes[cls_name]
            if counter.get(cls):
                counter[cls] += 1
            else:
                counter[cls] = 1

        self.counter = counter


    def save_objects(self, objects, storage_obj):
        storage_obj.reload()
        for obj in objects:
            #obj.updated_at = datetime.utcnow()
            storage_obj.new(obj)
        storage_obj.save()

    def get(self, cls):
        """Get the objects of class 'cls'."""
        ret = list()
        for obj in self.objects:
            if obj.__class__.__name__ == cls:
                ret.append(obj)
        return ret
        
