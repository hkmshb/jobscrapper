from datetime import datetime
from jobs.models import DurationUnit

HOUR_IN_SECONDS = 60 * 60
DAY_IN_SECONDS = 24 * HOUR_IN_SECONDS


def has_duration_elapsed(
    past_moment: datetime,
    duration: int,
    moment: datetime = datetime.now(),
    duration_unit: DurationUnit = DurationUnit.DAYS
) -> bool:
    """Checks whether a certain duration has elapsed between two given moments in time.

    :param past_moment: [description]
    :type past_moment: datetime
    :param duration: [description]
    :type duration: int
    :param moment: the moment in time to use in computing duration scraping has been
        paused for a company, defaults to datetime.now()
    :type moment: datetime, optional
    :param duration_unit: indicates how to interpret the configured update frequency for
        a company, defaults to DurationUnit.DAYS
    :type duration_unit: DurationUnit, optional
    :returns: True if duration has elapsed otherwise False
    :rtype: bool
    """
    total_seconds = int((moment - past_moment).total_seconds())
    deno = DAY_IN_SECONDS if duration_unit == DurationUnit.DAYS else HOUR_IN_SECONDS
    diff = int(total_seconds / deno)
    return diff >= duration
