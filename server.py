from flask import Flask, render_template, jsonify, request
from os import environ
import gork
import gunicorn

app = Flask(__name__)

# ROUTES
@app.route('/')
def index():
    return render_template('index.html', ssl=('DATABASE_URL' in environ))

@app.route('/geotest')
def geotest():
    return render_template('geotest.html')

@app.route('/scan',methods=['POST'])
def scan():
    try:
        # debug
        my_coords = tuple([float(request.form.get(coord)) for coord in ['lat', 'lon']])
        acc = float(request.form.get('acc'));
        return jsonify({
            'things': gork.look_around(my_coords)
        })
    except TypeError as e:
        return jsonify({'error': 'You\'re not my type, ' + e.strerror})
    except ValueError as e:
        return jsonify({'error': 'I don\'t value you, ' + e.strerror})

if __name__ == '__main__':
    app.run(debug=True, port=7001)
