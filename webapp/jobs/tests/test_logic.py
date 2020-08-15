from django.test import TestCase
from jobs.models import Opening


class OpeningTestCase(TestCase):
    fixtures = ['companies.json', 'openings.json']

    def test_find_opening_by_url(self):
        job_url = 'https://worldbankgroup.csod.com/ats/careersite/JobDetails.aspx?id=8313&site=1'
        opening = Opening.objects.get(url=job_url)
        self.assertIsNotNone(opening)
        self.assertEqual(opening.role_title, 'Senior Investment Officer | IFC | req8313')
