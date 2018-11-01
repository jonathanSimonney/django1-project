from django.test import TestCase
from django.urls import reverse

from .models import Pastebin
from .views import create_pastebin
# Create your tests here.


class PastebinFormTests(TestCase):
    def _post_data_to_view(self, post_data):
        self.client.post(reverse('pasteAsMarkdown:create_pastebin'), post_data)

    def _get_latest_pastebin(self):
        return Pastebin.objects.latest("id")

    def test_create_pastebin(self):
        """
        The pastebin may be created with a text and a path
        """
        self._post_data_to_view({"markdown_text": "# a title", "path": "url1"})
        latest_pastebin = self._get_latest_pastebin()
        self.assertEqual(latest_pastebin.path, "url1")
        self.assertEqual(latest_pastebin.markdown_text, "# a title")

    def test_create_pastebin_without_url(self):
        """
        The pastebin may be created with a text only, and a path should be auto generated
        """
        self._post_data_to_view({"markdown_text": "# a title", "path": ''})
        latest_pastebin = self._get_latest_pastebin()
        self.assertIsNotNone(latest_pastebin.path)
        self.assertNotEqual(latest_pastebin.path, "")
        self.assertEqual(latest_pastebin.markdown_text, "# a title")

    def test_create_pastebin_with_existing_url(self):
        """
        The pastebin may be created with a text and an already existing path,
         and a new path should be generated
        """
        self._post_data_to_view({"markdown_text": "# a title", "path": "url1"})
        self._post_data_to_view({"markdown_text": "# a different title", "path": "url1"})
        latest_pastebin = self._get_latest_pastebin()
        self.assertNotEqual(latest_pastebin.path, "url1")
        first_pastebin = Pastebin.objects.get(path="url1")
        self.assertEqual(first_pastebin.markdown_text, "# a title")
        self.assertEqual(latest_pastebin.markdown_text, "# a different title")
