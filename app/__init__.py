import config
from app.db import SQLDao
from flask import Flask

app = Flask(__name__)

app.config.from_object(config.DevelopmentConfig)

sql_general_dao = SQLDao()

from . import views
