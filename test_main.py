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

def test_login_success(client):
    # First register a user
    client.post('/signup',
                data=json.dumps({
                    'username': 'testuser',
                    'email': 'test@example.com',
                    'password': 'password123'
                }),
                content_type='application/json')
    
    # Then login
    response = client.post('/login',
                          data=json.dumps({
                              'username': 'testuser',
                              'password': 'password123'
                          }),
                          content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['message'] == 'ログインしました'

def test_login_invalid_credentials(client):
    response = client.post('/login',
                          data=json.dumps({
                              'username': 'nonexistent',
                              'password': 'wrongpass'
                          }),
                          content_type='application/json')
    
    assert response.status_code == 401

def test_profile_requires_login(client):
    response = client.get('/profile')
    assert response.status_code == 401

def test_reset_password_flow(client):
    # 1) Create user
    client.post('/signup',
                data=json.dumps({
                    'username': 'resetuser',
                    'email': 'reset@example.com',
                    'password': 'oldpassword123'
                }),
                content_type='application/json')
    
    # 2) Request password reset
    response = client.post('/reset-password-request',
                          data=json.dumps({
                              'email': 'reset@example.com'
                          }),
                          content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    token = data['token']
    
    # 3) Confirm password reset
    response = client.post('/reset-password-confirm',
                          data=json.dumps({
                              'token': token,
                              'password': 'newpassword123'
                          }),
                          content_type='application/json')
    
    assert response.status_code == 200
    
    # 4) Login with new password
    response = client.post('/login',
                          data=json.dumps({
                              'username': 'resetuser',
                              'password': 'newpassword123'
                          }),
                          content_type='application/json')
    
    assert response.status_code == 200

def test_reset_password_invalid_email(client):
    response = client.post('/reset-password-request',
                          data=json.dumps({
                              'email': 'nonexistent@example.com'
                          }),
                          content_type='application/json')
    
    assert response.status_code == 404

def test_reset_password_invalid_token(client):
    response = client.post('/reset-password-confirm',
                          data=json.dumps({
                              'token': 'invalid-token',
                              'password': 'newpassword123'
                          }),
                          content_type='application/json')
    
    assert response.status_code == 400