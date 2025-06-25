import unittest
from app import create_app

class TestAmenityEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_amenity_valid(self):
        """POST /api/v1/amenities/ with valid name should return 201"""
        response = self.client.post('/api/v1/amenities/', json={
            "name": "Wi-Fi"
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.get_json())
        self.assertIn("name", response.get_json())

    def test_get_all_amenities(self):
        """GET /api/v1/amenities/ should return 200 and a list"""
        response = self.client.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)

    def test_get_nonexistent_amenity(self):
        """GET /api/v1/amenities/<invalid_id> should return 404"""
        response = self.client.get('/api/v1/amenities/invalid-id')
        self.assertEqual(response.status_code, 404)
        self.assertIn("error", response.get_json())

    def test_update_amenity_valid(self):
        """PUT /api/v1/amenities/<id> with valid data should return 200"""
        # First create
        post = self.client.post('/api/v1/amenities/', json={"name": "Parking"})
        amenity_id = post.get_json().get("id")

        # Then update
        response = self.client.put(f'/api/v1/amenities/{amenity_id}', json={
            "name": "Free Parking"
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json().get("name"), "Free Parking")

if __name__ == '__main__':
    unittest.main()
