from django.test import SimpleTestCase
from django.urls import reverse, resolve
from EPG_creation.views import index, EPG




class TestUrls(SimpleTestCase):

    def test_index_url_resolves(self):
        url = reverse('index')
        print(resolve(url))
        self.assertEqual(resolve(url).func, index )

    def test_EPG_generator_url_resolves(self):
        url = reverse('epg_generator')
        resolver_match = resolve(url)
        self.assertEqual(resolver_match.func.__name__, EPG.as_view().__name__)
 
 