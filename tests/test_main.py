import pytest
import json
from app.main import app

@pytest.fixture
def client():
    """Create a test client for the app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json == {"status": "healthy"}

def test_greet_no_name(client):
    """Test greeting without name parameter."""
    response = client.get('/greet')
    assert response.status_code == 200
    assert response.json == {"message": "Hello, World!"}

def test_greet_with_name(client):
    """Test greeting with name parameter."""
    response = client.get('/greet?name=Alice')
    assert response.status_code == 200
    assert response.json == {"message": "Hello, Alice!"}

def test_greet_with_long_name(client):
    """Test greeting with name that's too long."""
    long_name = "A" * 51
    response = client.get(f'/greet?name={long_name}')
    assert response.status_code == 400
    assert response.json == {"error": "Name too long"}

def test_greet_xss_prevention(client):
    """Test that XSS attempts are sanitized."""
    malicious_name = "<script>alert('xss')</script>"
    response = client.get(f'/greet?name={malicious_name}')
    assert response.status_code == 200
    assert "<script>" not in response.json["message"]

def test_validate_url_valid(client):
    """Test URL validation with valid URL."""
    response = client.post('/validate-url',
                          data=json.dumps({"url": "https://example.com"}),
                          content_type='application/json')
    assert response.status_code == 200
    assert response.json["valid"] is True

def test_validate_url_invalid(client):
    """Test URL validation with invalid URL."""
    response = client.post('/validate-url',
                          data=json.dumps({"url": "javascript:alert(1)"}),
                          content_type='application/json')
    assert response.status_code == 200
    assert response.json["valid"] is False

def test_validate_url_missing(client):
    """Test URL validation with missing URL."""
    response = client.post('/validate-url',
                          data=json.dumps({}),
                          content_type='application/json')
    assert response.status_code == 400
    assert response.json == {"error": "Missing URL"}
