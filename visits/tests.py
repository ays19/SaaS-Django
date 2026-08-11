from django.test import TestCase
from visits.models import PageVisit

class PageVisitModelTests(TestCase):
    def test_create_page_visit(self):
        # Test that we can create a PageVisit and it gets a timestamp
        visit = PageVisit.objects.create(path="/test-path/")
        self.assertEqual(visit.path, "/test-path/")
        self.assertIsNotNone(visit.timestamp)
        self.assertEqual(PageVisit.objects.count(), 1)
