import unittest
from app import create_app

class TestUserEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_user_valid(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Alice",
            "last_name": "Smith",
            "email": "alice@example.com"
        })
        self.assertEqual(response.status_code, 201)

    def test_create_user_invalid_email(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Bob",
            "last_name": "Jones",
            "email": "invalid-email"
        })
        self.assertEqual(response.status_code, 400)

    def test_get_nonexistent_user(self):
        response = self.client.get('/api/v1/users/invalid-id')
        self.assertEqual(response.status_code, 404)
