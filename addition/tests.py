from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse

class AdditionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('add-numbers')

    def test_addition_success(self):
        request_data = {
            "batchid": "id0101",
            "payload": [[1, 2], [3, 4]]
        }
        response = self.client.post(self.url, request_data, format='json')
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data["batchid"], "id0101")
        self.assertEqual(response_data["response"], [3, 7])
        self.assertEqual(response_data["status"], "complete")
        self.assertIn("started_at", response_data)
        self.assertIn("completed_at", response_data)

    def test_addition_invalid_payload(self):
        request_data = {
            "batchid": "id0101",
            "payload": "invalid_payload"
        }
        response = self.client.post(self.url, request_data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_addition_empty_payload(self):
        request_data = {
            "batchid": "id0101",
            "payload": []
        }
        response = self.client.post(self.url, request_data, format='json')
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data["response"], [])
        self.assertEqual(response_data["status"], "complete")

    def test_addition_large_numbers(self):
        request_data = {
            "batchid": "id0101",
            "payload": [[1000000, 2000000], [3000000, 4000000]]
        }
        response = self.client.post(self.url, request_data, format='json')
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data["response"], [3000000, 7000000])
        self.assertEqual(response_data["status"], "complete")
