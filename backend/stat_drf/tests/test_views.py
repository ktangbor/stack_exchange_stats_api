from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class BasicStatResultsTestCase(APITestCase):

    def test_response_status(self):
        url = "%s?since=2022-01-05 12:00:00&until=2023-04-30 13:00:05" % reverse('stackstats-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
