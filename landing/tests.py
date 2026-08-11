from django.test import TestCase
from django.urls import reverse

class LandingViewTests(TestCase):
    def test_landing_page_status_code(self):
        # Test that the landing page renders successfully for anonymous users
        url = reverse("home")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "landing/main.html")
        self.assertContains(response, "page views")
