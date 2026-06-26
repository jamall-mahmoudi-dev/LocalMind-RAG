from django.urls import reverse
from rest_framework.test import APITestCase


class HealthCheckTests(APITestCase):
    def test_health_endpoint_returns_ok(self):
        url = reverse("health")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("status", response.data)
