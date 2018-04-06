from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from os import environ
import gork
import gunicorn

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ['DATABASE_URL']
db = SQLAlchemy(app)
logman = LoginManager()
logman.init_app(app)
game = gork.Gork()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/geotest')
def geotest():
    return render_template('geotest.html')

@app.route('/scan',methods=['POST'])
def scan():
    try:
        my_coords = tuple([float(request.form.get(coord)) for coord in ['lat', 'lon']])
        acc = float(request.form.get('acc'));
        return jsonify({
            'things': [ # TODO flytta till gork
                {'dist': gork.dist(my_coords, thing.coords), 'name': thing.name}
                for thing in game.world
            ]
        })
    except (TypeError, ValueError):
        return jsonify({'error': 'your parameters are bad and you should feel bad'})


if __name__ == '__main__':
    app.run(debug=True, port=7001)
