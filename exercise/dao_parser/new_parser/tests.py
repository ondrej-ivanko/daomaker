from django.test import TestCase


class TestViews(TestCase):
    def test_list(self):
        response = self.client.get("items/")
        self.assertEqual(response.status_code, 200)

