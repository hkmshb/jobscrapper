from datetime import datetime

from django.test import TestCase
from parameterized import parameterized

from jobs.models import DurationUnit
from jobs.utils import has_duration_elapsed


def tod(value: str) -> datetime:
    """tod (aka to date) converts date string to datetime objectt.

    :param value: date string value to convert
    :type value: str
    :return: datetime object
    :rtype: datetime
    """
    return datetime.fromisoformat(value)


class UtilTests(TestCase):

    @parameterized.expand([
        (tod('2020-08-01 00:00:00'), tod('2020-08-02 23:00:00'), 2, DurationUnit.DAYS, False),
        (tod('2020-08-01 00:01:00'), tod('2020-08-02 23:59:00'), 2, DurationUnit.DAYS, False),
        (tod('2020-08-01 00:00:00'), tod('2020-08-03 00:00:00'), 2, DurationUnit.DAYS, True),
        (tod('2020-08-01 00:00:00'), tod('2020-07-30 00:00:00'), 2, DurationUnit.DAYS, False),
        (tod('2020-08-01 00:00:00'), tod('2020-08-01 01:00:00'), 2, DurationUnit.HOURS, False),
        (tod('2020-08-01 00:00:00'), tod('2020-08-01 05:00:00'), 2, DurationUnit.HOURS, True),
        (tod('2020-08-01 00:00:00'), tod('2020-08-02 00:00:00'), 2, DurationUnit.HOURS, True),
    ])
    def test_has_duration_elapsed(
        self,
        past_moment: datetime,
        moment: datetime,
        duration: int,
        duration_unit: DurationUnit,
        expected: bool
    ):
        result = has_duration_elapsed(past_moment, duration, moment, duration_unit)
        self.assertEqual(result, expected)
