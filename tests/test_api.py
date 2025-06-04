from fastapi.testclient import TestClient
from app.main import app
import pytest


@pytest.fixture
def client():
    # ensure DB tables exist
    from app.database import init_db
    init_db()
    with TestClient(app) as c:
        yield c

def test_root(client):
    r = client.get('/')
    assert r.status_code == 200

def test_evaluate(client):
    r = client.post('/api/evaluate', json={'prompt': 'hello'})
    assert r.status_code == 200
    data = r.json()
    assert 'results' in data
    assert len(data['results']) == 2

def test_register_login_and_eval(client):
    reg = client.post('/register', json={'username': 'alice', 'password': 'pw'})
    assert reg.status_code == 200
    token = reg.json()['access_token']

    login = client.post('/login', data={'username': 'alice', 'password': 'pw'})
    assert login.status_code == 200
    token2 = login.json()['access_token']
    assert token2

    r = client.post('/api/evaluate', json={'prompt': 'hi'}, headers={'Authorization': f'Bearer {token2}'})
    assert r.status_code == 200
    data = r.json()
    assert 'results' in data


def test_admin_model_management(client):
    # register admin
    reg = client.post('/register', json={'username': 'admin', 'password': 'pw', 'is_admin': True})
    assert reg.status_code == 200
    token = reg.json()['access_token']

    # list models
    r = client.get('/admin/models', headers={'Authorization': f'Bearer {token}'})
    assert r.status_code == 200
    count = len(r.json())

    # add a new model
    add = client.post(
        '/admin/models',
        json={'name': 'Echo2', 'type': 'echo'},
        headers={'Authorization': f'Bearer {token}'},
    )
    assert add.status_code == 200
    mid = add.json()['id']

    # ensure count increased
    r2 = client.get('/admin/models', headers={'Authorization': f'Bearer {token}'})
    assert len(r2.json()) == count + 1

    # delete model
    delr = client.delete(f'/admin/models/{mid}', headers={'Authorization': f'Bearer {token}'})
    assert delr.status_code == 200
