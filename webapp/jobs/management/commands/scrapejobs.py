import sys
from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from django.utils import timezone

from jobs.models import Company, DurationUnit
from jobs.utils import has_duration_elapsed


class Command(BaseCommand):
    """
    :opt --company: indicates company to be scrapped by registered shortname for the
        company; when not provided entire registered companies are scraped
    :opt --freq-unit (minute, hours, days): indicates how to interpret the values set
        for update_freq; in minutes, hours or days. defaults to days
    :opt --ignore-update-freq boolean: causes all listed companies to be scrapped
        ignoring the update freq settings
    """

    help = 'Scrap job openings from job listing pages of register companies'

    def add_arguments(self, parser):
        parser.add_argument(
            '-c',
            '--company',
            action='append',
            help='name slug for a known/registered company to scrap'
        )

        parser.add_argument(
            '-f',
            '--freq-unit',
            choices=DurationUnit.values(),
            default=DurationUnit.DAYS.value,
            help='indicates how DurationUnits for update frequency is to be interpreted'
        )

        parser.add_argument(
            '-i',
            '--ignore-update-freq',
            action='store_true',
            default=False,
            help='indicates whether to ignore update frequency settings for companies'
        )

    def should_scrape(self, company: Company, freq_unit: str):
        """Determines whether to scrape company based on configured update frequency

        :param company: the company whose vacancies are to be scraped
        :type company: Company
        """

    def allow_scraping(
        self,
        company: Company,
        moment: datetime,
        freq_unit: DurationUnit
    ) -> bool:
        """Determines whether scraping should be allowed for a company as at the moment
        check was made. Scraping is allowed if it has never been done for the company or
        if certain duration has elapsed.

        :param company: the company to assess whether to be scraped
        :type company: Company
        :param moment: the moment to compute elapsed duration since last scrape against
        :type moment: datetime
        :param freq_unit: the unit for the duration which can be in days or hours
        :type freq_unit: DurationUnit
        :return: True if scraping it to be allowed otherwise False
        :rtype: bool
        """
        if not company.last_updated:
            return True

        return has_duration_elapsed(
            company.last_updated,
            company.update_freq,
            moment,
            freq_unit
        )

    def handle(self, *args, **options):
        name_slugs = options['company']
        query = Q() if not name_slugs else Q(name_slug__in=name_slugs)
        companies = Company.objects.filter(query)

        if name_slugs and len(companies) != len(name_slugs):
            unknowns = list(filter(
                lambda slug: slug not in [c.name_slug for c in companies],
                name_slugs
            ))
            raise CommandError(f"scraper:: Unknown company name slug(s): {', '.join(unknowns)}")

        # determine companies that should be scraped
        ignore_update_freq = options['ignore_update_freq']
        if not ignore_update_freq:
            freq_unit = DurationUnit(options['freq_unit'])
            moment = timezone.now()

            companies = list(filter(
                lambda c: self.allow_scraping(c, moment, freq_unit),
                companies
            ))

        if not companies:
            self.stdout.write('scraper:: No companies up for scraping at this time')
            sys.exit(0)

        ref = 'company' if len(companies) == 1 else 'companies'
        self.stdout.write(f'scraper:: {len(companies)} {ref} up for scraping')
