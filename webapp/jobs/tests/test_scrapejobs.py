import itertools
from io import StringIO

from django.core.management.base import CommandError
from django.core.management import call_command
from django.test import TestCase

from parameterized import parameterized

class ScrapeJobsTests(TestCase):
    fixtures = ['companies.json']

    @parameterized.expand([
        (['world-bank-xyz', 'seq-uoai'], 'world-bank-xyz, seq-uoai'),
        (['world-bank-xyz', 'sequoai'], 'world-bank-xyz'),
        (['world-bank-group', 'seq-uoai'], 'seq-uoai'),
    ])
    def test_command_fails_for_unknown_company_name_slugs(self, name_slugs, bad_names):
        err = StringIO()
        commands = [['-c', name_slug] for name_slug in name_slugs]
        flatten = list(itertools.chain.from_iterable(commands))

        with self.assertRaises(CommandError) as ex:
            call_command('scrapejobs', *flatten, stderr=err)

        errmsg_prefix = 'Unknown company name slug(s):'
        self.assertIn(f'{errmsg_prefix} {bad_names}', str(ex.exception))
