from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from os import environ
from os.path import abspath
import gork
import gunicorn

app = Flask('gork')
if 'DATABASE_URL' in environ:
    print('running live')
    app.config['SQLALCHEMY_DATABASE_URI'] = environ['DATABASE_URL']
else:
    print('running locally')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + abspath('dev.db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
logman = LoginManager()
logman.init_app(app)

from routes import *

if __name__ == '__main__':
    app.run(debug=True, port=7001)
