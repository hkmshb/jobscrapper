from copy import deepcopy
from parameterized import parameterized

from django.db.models import Q
from django.forms.models import model_to_dict
from django.test import TestCase
from glom import glom

from jobs.models import Company, Opening
from jobs.logic import opening_insert, opening_update
from jobs.exceptions import JobsError, OpeningExistError


class OpeningTestBase(TestCase):
    fixtures = ['companies.json', 'openings.json']

    NEW_OPENING = {
        'company': '?',
        'job': {
            'url': 'https://foo.bar/jobs',
            'role_title': 'Foo Bar Job',
            'description': 'A job to do Foo Bar',
            'date_active': '2020-09-16'
        }
    }


class OpeningTestCase(OpeningTestBase):

    def test_find_opening_by_url(self):
        job_url = 'https://worldbankgroup.csod.com/ats/careersite/JobDetails.aspx?id=8313&site=1'
        opening = Opening.objects.get(url=job_url)
        self.assertIsNotNone(opening)
        self.assertEqual(opening.role_title, 'Senior Investment Officer | IFC | req8313')

    @parameterized.expand([
        ({'company': '?', 'job': {'description': 'description changed'}}, 1, False),
        ({'company': '?', 'job': {'role_title': 'title changed'}}, 1, False),
        ({'company': '?', 'job': {'date_active': '2020-08-16'}}, 1, True),
        ({'company': '?', 'job': {'date_inactive': '2020-08-16'}}, 1, True),
        ({'company': '?', 'job': {'date_created': '2020-08-16'}}, 1, True)
    ])
    def test_is_match(self, data, pkey, expected):
        opening = Opening.objects.get(pk=pkey)
        self.assertIsNotNone(opening)
        self.assertEqual(opening.is_match(data), expected)


class OpeningInsertTestCase(OpeningTestBase):

    def test_succeeds_when_opening_url_not_in_database(self):
        data = deepcopy(self.NEW_OPENING)
        data['company'] = Company.objects.first()

        spec = 'job.url'
        found_count = Opening.objects.filter(url=glom(data, spec)).count()
        self.assertEqual(found_count, 0)

        opening = opening_insert(data)
        self.assertIsNotNone(opening)
        self.assertTrue(opening.id != 0)
        self.assertEqual(opening.url, glom(data, spec))

    def test_fails_when_opening_url_in_database(self):
        data = deepcopy(self.NEW_OPENING)
        data['company'] = Company.objects.first()
        data['job']['url'] = 'https://foo.bar/jobs/v2'
        data['job']['role_title'] = 'Foo Bar Job (v2)'

        # ensure job with url already exist in the db
        found_count = Opening.objects.filter(url=glom(data, 'job.url')).count()
        if not found_count:
            opening = opening_insert(data)
            self.assertIsNotNone(opening)

        # attempt insert data (any data) with existing
        with self.assertRaises(OpeningExistError):
            opening_insert(data)


class OpeningUpdateTestCase(OpeningTestBase):

    def _get_opening_with_data(self):
        opening = Opening.objects.first()
        data = deepcopy({
            'company': opening.company,
            'job': model_to_dict(opening)
        })

        return (opening, data)

    def test_fails_when_job_url_change_attempted(self):
        # never allow the job_url for an opening to be changed
        opening, data = self._get_opening_with_data()
        data['job']['url'] = 'https://foo.bar/jobs/changed'
        with self.assertRaises(JobsError):
            opening_update(opening, data)

    def test_fails_when_company_change_attempted(self):
        opening, data = self._get_opening_with_data()
        company = Company.objects.filter(~Q(id=opening.company.id)).first()
        self.assertIsNotNone(company)

        # use different company
        data['company'] = data['job']['company'] = company
        with self.assertRaises(JobsError):
            opening_update(opening, data)

    def test_succeeds_for_valid_field_changes(self):
        opening, data = self._get_opening_with_data()
        old_description = opening.description

        # change description
        data['job']['description'] = 'I got changed'
        upd_opening = opening_update(opening, data)

        self.assertIsNotNone(upd_opening)
        self.assertEqual(upd_opening.id, opening.id)
        self.assertEqual(upd_opening.url, opening.url)
        self.assertNotEqual(old_description, opening.description)
