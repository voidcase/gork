from server import app
import pytest


@pytest.fixture
def tester():
    return app.test_client()

@pytest.mark.parametrize('route', [
    ('/', 200),
    ('/login', 200),
    ('/register', 200),
    ('/geotest', 200),
    ('/logout', 401)
    ])
def test_public_get_status_ok(tester, route):
    res = tester.get('/',content_type='html/text')
    assert res.status_code == 200

def test_scan(tester):
    import json
    res = tester.post('/scan', data=dict(
            lat=0.0,
            lon=0.0,
            acc=10
        ))
    assert res.status_code == 200
    assert 'error' not in json.loads(res.data)

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
