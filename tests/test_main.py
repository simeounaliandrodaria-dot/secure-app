import pytest
import json
from app.main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json == {"status": "healthy"}

def test_greet_no_name(client):
    response = client.get('/greet')
    assert response.status_code == 200
    assert response.json == {"message": "Hello, World!"}

def test_greet_with_name(client):
    response = client.get('/greet?name=Alice')
    assert response.status_code == 200
    assert response.json == {"message": "Hello, Alice!"}

def test_greet_with_long_name(client):
    long_name = "A" * 51
    response = client.get(f'/greet?name={long_name}')
    # This assertion will FAIL because the main.py code is missing the length check
    assert response.status_code == 400
    assert response.json == {"error": "Name too long"}

def test_greet_xss_prevention(client):
    malicious_name = "<script>alert('xss')</script>"
    response = client.get(f'/greet?name={malicious_name}')
    assert response.status_code == 200
    assert "<script>" not in response.json["message"]

def test_validate_url_valid(client):
    response = client.post('/validate-url',
                          data=json.dumps({"url": "https://example.com"}),
                          content_type='application/json')
    assert response.status_code == 200
    assert response.json["valid"] is True

def test_validate_url_invalid(client):
    response = client.post('/validate-url',
                          data=json.dumps({"url": "javascript:alert(1)"}),
                          content_type='application/json')
    assert response.status_code == 200
    assert response.json["valid"] is False

def test_validate_url_missing(client):
    response = client.post('/validate-url',
                          data=json.dumps({}),
                          content_type='application/json')
    assert response.status_code == 400
    assert response.json == {"error": "Missing URL"}
