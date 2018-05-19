from server import app
import pytest
import flask_login
import gorkdata as db
import re


app.config['TESTING'] = True
app.config['WTF_CSRF_METHODS'] = []
app.config['WTF_CSRF_ENABLED'] = False
db.reset_db()


@pytest.fixture
def tester():
    return app.test_client()


@pytest.fixture
def treasure_of_null_island():
    t = db.Treasure.create(
            node=db.Node.create(lat=0,lon=0,name='Treasure of null island'),
            contents=100000
            ) 
    yield t
    t.delete()


def login(client, username, password):
    return client.post('/login',
            data=dict(
                username=username,
                password=password,
                ),
            follow_redirects=True)


@pytest.mark.parametrize('route', [
    ('/', 200),
    ('/login', 200),
    ('/register', 200),
    ('/geotest', 200),
    ('/logout', 401),
    ('/game', 401),
    ])
def test_public_get_status_ok(tester, route):
    res = tester.get(route[0],content_type='html/text')
    assert res.status_code == route[1]


def test_login(tester):
    logres = login(tester,'Aaa','aaaaaaaaa')
    assert logres.status_code == 200
    assert b'nah' not in logres.data


def test_register(tester):
    res1 = tester.post('/register',data=dict(
        username='bbb',
        email='bbb@bbb.bbb',
        password='bbbbbbbbb'
        ), follow_redirects=True)
    assert res1.status_code == 200
    assert b'bbb' in res1.data
    u = db.User.get(name='bbb')
    assert u
    db.User.delete_by_id(u.id)


def test_scan(tester):
    import json
    logres = login(tester,'Aaa','aaaaaaaaa')
    res = tester.post('/scan', data=dict(
            lat=0.0,
            lon=0.0,
            acc=10
        ))
    assert res.status_code == 200
    assert 'error' not in json.loads(res.data)
    assert 'things' in json.loads(res.data)

def test_dig(tester, treasure_of_null_island):
    import json
    logres = login(tester,'Aaa','aaaaaaaaa')
    res = tester.post('/dig', data=dict(
            lat=0.0,
            lon=0.0,
            acc=10
        ))
    assert res.status_code == 200
    resdata = json.loads(res.data)
    assert 'error' not in resdata
    assert resdata['found'] == 100000
    t = db.Treasure.get(node=treasure_of_null_island.node)
    assert t.contents == 0
    res2 = tester.post('/dig', data=dict(
            lat=0.0,
            lon=0.0,
            acc=10
        ))
    assert res2.status_code == 200
    resdata2 = json.loads(res2.data)
    assert 'error' not in resdata2
    assert resdata2['found'] == 0


def test_card_dir():
    from gork import card_dir
    assert card_dir((0,0),( 1, 0)) == 'N'
    assert card_dir((0,0),(-1, 0)) == 'S'
    assert card_dir((0,0),( 0, 1)) == 'E'
    assert card_dir((0,0),( 0,-1)) == 'W'
    assert card_dir((0,0),( 1, 1)) == 'NE'
    assert card_dir((0,0),(-1, 1)) == 'SE'
    assert card_dir((0,0),( 1,-1)) == 'NW'
    assert card_dir((0,0),(-1,-1)) == 'SW'
