from geopy.distance import vincenty

class Node:
    def __init__(self, coords, name):
        self.coords = coords
        self.name = name

def dist(a, b):
    return round(vincenty(a,b).meters)

class Gork:
    def __init__(self):
        self.world = [
                Node((55.723533, 13.214179), "magic oval"),
                Node((55.723367, 13.206387), "mystical clearing")
                ]
