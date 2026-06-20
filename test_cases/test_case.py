import pytest
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


# ----------------------------
# Frontend Route
# ----------------------------
def test_index(client):
    response = client.get('/')
    assert response.status_code == 200


# ----------------------------
# /api/submit Tests
# ----------------------------
def test_submit_success(client):
    response = client.post(
        '/api/submit',
        json={'username': 'Prajwal'}
    )

    data = response.get_json()

    assert response.status_code == 200
    assert data['status'] == 'success'
    assert 'Welcome aboard' in data['message']


def test_submit_empty_username(client):
    response = client.post(
        '/api/submit',
        json={'username': ''}
    )

    data = response.get_json()

    assert response.status_code == 400
    assert data['status'] == 'error'


# ----------------------------
# /api/stats Tests
# ----------------------------
def test_get_stats(client):
    response = client.get('/api/stats')

    data = response.get_json()

    assert response.status_code == 200
    assert data['status'] == 'success'
    assert 'data' in data
    assert 'active_users' in data['data']


# ----------------------------
# /api/toggle-theme Tests
# ----------------------------
def test_toggle_theme(client):
    response = client.post(
        '/api/toggle-theme',
        json={'theme': 'light'}
    )

    data = response.get_json()

    assert response.status_code == 200
    assert data['status'] == 'success'
    assert data['applied_theme'] == 'light'


def test_toggle_theme_default(client):
    response = client.post(
        '/api/toggle-theme',
        json={}
    )

    data = response.get_json()

    assert response.status_code == 200
    assert data['applied_theme'] == 'dark'


# ----------------------------
# /health Tests
# ----------------------------
def test_health_check(client):
    response = client.get('/health')

    data = response.get_json()

    assert response.status_code == 200
    assert data['status'] == 'healthy'
    assert 'uptime_seconds' in data
    assert 'services' in data
```
