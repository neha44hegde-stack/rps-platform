from app.models import User

def test_register_creates_user(client, db):
    response = client.post('/register', data={
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'password123',
        'confirm_password': 'password123'
    }, follow_redirects=True)

    assert response.status_code == 200
    user = User.query.filter_by(username='testuser').first()
    assert user is not None
    assert user.email == 'testuser@example.com'

def test_password_is_hashed(client, db):
    client.post('/register', data={
        'username': 'hashcheck',
        'email': 'hashcheck@example.com',
        'password': 'password123',
        'confirm_password': 'password123'
    })
    user = User.query.filter_by(username='hashcheck').first()
    assert user.password_hash != 'password123'
    assert user.check_password('password123')
    assert not user.check_password('wrongpassword')

def test_login_with_correct_credentials(client, db):
    client.post('/register', data={
        'username': 'loginuser',
        'email': 'loginuser@example.com',
        'password': 'password123',
        'confirm_password': 'password123'
    })
    response = client.post('/login', data={
        'username': 'loginuser',
        'password': 'password123'
    }, follow_redirects=True)
    assert response.status_code == 200

def test_login_with_wrong_password_fails(client, db):
    client.post('/register', data={
        'username': 'wrongpass',
        'email': 'wrongpass@example.com',
        'password': 'password123',
        'confirm_password': 'password123'
    })
    response = client.post('/login', data={
        'username': 'wrongpass',
        'password': 'incorrectpassword'
    }, follow_redirects=True)
    assert b'Invalid username or password' in response.data
