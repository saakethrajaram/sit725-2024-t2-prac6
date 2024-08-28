import unittest
from auth_app import app, users_db  

class TestAuthApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        users_db.clear()  

    def test_register_user(self):
        response = self.app.post('/register', json={'username': 'testuser', 'password': 'Password123'})
        print("Test Register User Response:", response.get_json())  
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['message'], 'User registered successfully!')

    def test_register_existing_user(self):
        # Register once
        self.app.post('/register', json={'username': 'testuser', 'password': 'Password123'})
        # Register again
        response = self.app.post('/register', json={'username': 'testuser', 'password': 'Password123'})
        print("Test Register Existing User Response:", response.get_json())
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data['error'], 'User already exists.')

    def test_login_user(self):
        # Register a new user first
        self.app.post('/register', json={'username': 'testuser', 'password': 'Password123'})
        # Login with the same user
        response = self.app.post('/login', json={'username': 'testuser', 'password': 'Password123'})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['message'], 'Logged in successfully!')

    def test_login_invalid_user(self):
        response = self.app.post('/login', json={'username': 'invaliduser', 'password': 'WrongPass123'})
        self.assertEqual(response.status_code, 401)
        data = response.get_json()
        self.assertEqual(data['error'], 'Invalid username or password.')

    def test_protected_route_access(self):
        # Register and login to set the session
        self.app.post('/register', json={'username': 'testuser', 'password': 'Password123'})
        self.app.post('/login', json={'username': 'testuser', 'password': 'Password123'})
        # Access the protected route
        response = self.app.get('/protected')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('Hello, testuser!', data['message'])

    def test_protected_route_unauthorized_access(self):
        response = self.app.get('/protected')
        self.assertEqual(response.status_code, 401)
        data = response.get_json()
        self.assertEqual(data['error'], 'Unauthorized access, please login.')

    def test_logout_user(self):
        # Register, login, then logout
        self.app.post('/register', json={'username': 'testuser', 'password': 'Password123'})
        self.app.post('/login', json={'username': 'testuser', 'password': 'Password123'})
        response = self.app.post('/logout')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['message'], 'Logged out successfully!')

if __name__ == '__main__':
    unittest.main()