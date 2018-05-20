from geopy.distance import distance
from gorkdata import Node, User, Treasure, LAT, LON, db
import config as cfg
import random
from math import pi, atan2

def dist(a:tuple, b:tuple) -> float:
    return round(distance(a,b).meters)

def card_dir(frm:tuple, to:tuple):
    dx = to[LON]-frm[LON]
    dy = to[LAT]-frm[LAT]
    angle = atan2(dy, dx)
    s = pi/8.0 # slice
    print("DBG: dx:",dx,"dy:",dy,"angle:",angle)
    if angle < -7*s or angle >= 7*s: return 'W'
    if angle < -5*s: return 'SW'
    if angle < -3*s: return 'S'
    if angle < -1*s: return 'SE'
    if angle <  1*s: return 'E'
    if angle <  3*s: return 'NE'
    if angle <  5*s: return 'N'
    if angle <  7*s: return 'NW'

def pick_rand(lst):
    return lst[random.randrange(len(lst))]


def generate_around(coords, dist, population):
    origo_lat = coords[LAT]
    origo_lon = coords[LON]
    with db.atomic():
        for i in range(population):
            n = Node.create(
                    lat=origo_lat + (random.random()-.5)*2*dist,
                    lon=origo_lon + (random.random()-.5)*2*dist,
                    name=pick_rand(cfg.NODE_ADJECTIVES)+" "+pick_rand(cfg.NODE_NOUNS),
                    )
            t = Treasure.create(
                    node=n,
                    contents=random.randint(1,100),
                    )
            print("generated a",n.name)


def look_around(from_coords):
    # visible_things = []
    # for node in Node.select():
    #     dist_to_node = dist(from_coords, node.coords())
    #     if dist_to_node <= look_range:
    #         thing = {
    #             'dist': dist_to_node,
    #             'dir': card_dir(from_coords, node.coords()),
    #             'name': node.name
    #             }
    #         if dist_to_node <= interact_range and Treasure.get(node=node.id):
    #             thing['treasure'] = True;
    #         visible_things.append(thing)
    return [
        {
            'dist': dist(from_coords, node.coords()),
            'dir': card_dir(from_coords, node.coords()),
            'name': node.name,
        }
        for node in Node.select() if dist(from_coords, node.coords()) <= cfg.RANGE_LOOK #TODO optimize
    ]


def dig_at(pos:tuple, user:User):
    for t in Treasure.select():
        if dist(pos,t.node.coords()) <= cfg.RANGE_INTERACT:
            user.gold += t.contents
            found = t.contents
            t.contents = 0
            user.save()
            t.save()
            return {'found':found}
    return {'found':0}

