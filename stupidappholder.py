from flask import Flask
from os import environ
from os.path import abspath
app = Flask(__name__)
if 'DATABASE_URL' in environ:
    print('running live')
    app.config['SQLALCHEMY_DATABASE_URI'] = environ['DATABASE_URL']
else:
    print('running locally')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + abspath('dev.db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
