"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group
from django.test import TestCase, Client

class SimpleTest(TestCase):
    def test_tram_station(self):
        """
        Tests tramway station
        """

        client = Client()

        response = client.get('/tramway_station/2.56/65.3/')
        self.assertEqual(response.status_code, 200)
