#!/usr/bin/python3
import sys
import os
import logging

logging.basicConfig(stream=sys.stderr)

sys.path.append("/var/www/bot_administration/")

# Fired up virtualenv before include application
activate_env = os.path.expanduser(os.path.join(os.path.dirname(__file__), 'venv/bin/activate_this.py'))
exec(open(activate_env).read()) # https://stackoverflow.com/questions/436198/what-is-an-alternative-to-execfile-in-python-3

from main import app as application
