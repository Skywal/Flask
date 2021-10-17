import os

app_dir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'A SECRET KEY'
    SQLACHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'YOU_MAIL@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'password'
    MAIL_DEFAULT_SENDER = MAIL_USERNAME

class DevelopementConfig(BaseConfig):
    DEBUG = True
    SQLACHEMY_DATABASE_URI = os.environ.get('DEVELOPMENT_DATABASE_URI') or \
        'mysql+pymysql://root:pass@localhost/flask_app_db'

class TestingConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TESTING_DATABASE_URI') or \
			      'mysql+pymysql://root:pass@localhost/flask_app_db'

class ProductionConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('PRODUCTION_DATABASE_URI') or \
	'mysql+pymysql://root:pass@localhost/flask_app_db'

# https://pythonru.com/uroki/19-struktura-i-jeskiz-prilozhenija-flask
