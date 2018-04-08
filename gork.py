from geopy.distance import vincenty
from gorkdata import db, Node

def dist(a:tuple, b:tuple) -> float:
    return round(vincenty(a,b).meters)

def look_around(from_coords):
    return [
        {
            'dist': dist(from_coords, node.coords()),
            'name': node.name
        }
        for node in Node.query.all()
    ]

