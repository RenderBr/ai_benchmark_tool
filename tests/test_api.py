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
