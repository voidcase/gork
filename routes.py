from flask import render_template, request, jsonify
from stupidappholder import app
import gork

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
