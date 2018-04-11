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
