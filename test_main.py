import pytest
import json
import tempfile
import os
from main import app, init_db

@pytest.fixture
def client():
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client
    
    os.close(db_fd)
    os.unlink(app.config['DATABASE'])

def test_signup_success(client):
    response = client.post('/signup', 
                          data=json.dumps({
                              'username': 'testuser',
                              'email': 'test@example.com',
                              'password': 'password123'
                          }),
                          content_type='application/json')
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['message'] == 'ユーザーが正常に作成されました'

def test_signup_missing_fields(client):
    response = client.post('/signup',
                          data=json.dumps({
                              'username': 'testuser'
                          }),
                          content_type='application/json')
    
    assert response.status_code == 400

def test_signup_duplicate_username(client):
    # First registration
    client.post('/signup',
                data=json.dumps({
                    'username': 'testuser',
                    'email': 'test1@example.com',
                    'password': 'password123'
                }),
                content_type='application/json')
    
    # Duplicate username
    response = client.post('/signup',
                          data=json.dumps({
                              'username': 'testuser',
                              'email': 'test2@example.com',
                              'password': 'password456'
                          }),
                          content_type='application/json')
    
    assert response.status_code == 409