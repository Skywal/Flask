import os
from app import app
from flask_script import Manager, Shell
#from flask_migrate import MigrateCommand

manager = Manager(app)

if __name__ == '__main__':
    manager.run(host='0.0.0.0')
