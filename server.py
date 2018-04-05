from flask import Flask, render_template, request, jsonify
import gork
import gunicorn
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan')
def scan():
    try:
        my_coords = tuple([float(request.form.get(coord)) for coord in ['lon', 'lat']])
        confidence = float(request.form.get('confidence'));
        return jsonify({
            'things': [
                {'dist': gork.dist(my_coords, thing.coords), 'name': thing.name}
                for thing in game.world
            ]
        })
    except (TypeError, ValueError):
        return jsonify({'error': 'your parameters are bad and you should feel bad'})


if __name__ == '__main__':
    app.run(debug=True, port=7001)
