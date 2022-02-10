import os

app_dir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    SECRET_KEY = os.environ.get('SEKRET_KEY') or 'a secret key'


class DevelopmentConfig(BaseConfig):
    DEBUG = True


# https://flask.palletsprojects.com/en/2.0.x/config/

is_debug = True

db_config = {'host': 'localhost',
             'user': 'main',
             'password': 'cat_doge',
             'db': 'framework'
             }