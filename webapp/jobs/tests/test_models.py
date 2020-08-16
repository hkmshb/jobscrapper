from django.test import TestCase

from jobs.models import Company


class CompanyTestCase(TestCase):

    def test_auto_assignment_of_name_slug_on_save(self):
        data = {
            'name': 'Test Company',
            'industry': 'Services',
            'vacancies_url': 'http://test-company.com/jobs',
            'last_updated': '2020-08-16',
        }
        company = Company(**data)
        self.assertIsNone(company.id)
        self.assertIn(company.name_slug, ('', None))

        company.save()
        self.assertTrue(company.id != 0)
        self.assertNotIn(company.name_slug, ('', None))
