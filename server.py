from flask import Flask, render_template, jsonify, request
from os import environ
from os.path import abspath
import gork
import gunicorn

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True, port=7001)
