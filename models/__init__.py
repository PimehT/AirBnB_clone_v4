#!/usr/bin/python3
"""
initialize the models package
"""

from os import getenv, environ


TEST_PATH = '/tmp/test_file.json'

storage_t = getenv("HBNB_TYPE_STORAGE")

# set storage type
if getenv('HBNB_ENV') == 'test':
    from models.engine.file_storage import FileStorage
    FileStorage._FileStorage__file_path = TEST_PATH
    environ['HBNB_MYSQL_DB'] = 'hbnb_test_db'

if storage_t == "db":
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
storage.reload()
