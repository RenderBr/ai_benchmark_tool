from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    r = client.get('/')
    assert r.status_code == 200

def test_evaluate():
    r = client.post('/api/evaluate', json={'prompt': 'hello'})
    assert r.status_code == 200
    data = r.json()
    assert 'results' in data
    assert len(data['results']) == 2

def test_register_login_and_eval():
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
