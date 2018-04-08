from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from os import environ
from os.path import abspath
import gork
import gunicorn
import psycopg2


# CONFIG
def create_app():
    app = Flask(__name__)
    if 'DATABASE_URL' in environ:
        print('running live')
        app.config['SQLALCHEMY_DATABASE_URI'] = environ['DATABASE_URL']
    else:
        print('running locally')
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + abspath('dev.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    with app.app_context():
        gork.db.init_app(app)
    return app

app = create_app()

# ROUTES
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
            'things': gork.look_around(my_coords)
        })
    except (TypeError, ValueError):
        return jsonify({'error': 'your parameters are bad and you should feel bad'})

@app.route('/init',methods=['POST'])
def init():
    from initdb import create_db
    create_db()
    return "and so it begins"

if __name__ == '__main__':
    app.run(debug=True, port=7001)
