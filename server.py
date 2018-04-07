from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from os import environ
from os.path import abspath
import gork
import gunicorn
from stupidappholder import app
logman = LoginManager()
logman.init_app(app)

from routes import *

if __name__ == '__main__':
    app.run(debug=True, port=7001)
