from django.test import TestCase, RequestFactory
from django.urls import reverse
from EPG_creation.models import Listing
from EPG_creation.views import EPG
import json

class EPGTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_get(self):
        request = self.factory.get(reverse('epg_generator'))
        response = EPG.as_view()(request)
        self.assertEqual(response.status_code, 200)
        

    def test_post_with_valid_data(self):
        data = {
            'file': 'test.csv',
            'custom_filename': 'custom_filename'
        }

        request = self.factory.post(reverse('epg_generator'), data)
        response = EPG.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Listing.objects.exists())

    def test_post_missing_valid_data(self):
        data = {
            'custom_filename': 'custom_filename'
        }

        request = self.factory.post(reverse('epg_generator'), data)
        response = EPG.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Listing.objects.exists())





