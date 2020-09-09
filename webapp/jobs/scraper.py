"""Defines objects for handling data scraping.
"""
import hashlib
import logging
import time

from collections import namedtuple
from dataclasses import dataclass
from datetime import datetime
from functools import reduce
from urllib.parse import urljoin
from typing import Dict, Iterable, List

from django.db import connection
from requests_html import Element, HTMLResponse, HTMLSession
from jobs.models import Company, Location, Opening


log = logging.getLogger(__name__)

Job = namedtuple('Job', ['data', 'hash', 'page_no'])
JobDetail = namedtuple('JobDetail', [
    'company', 'locations', 'entry_hash', 'role_title', 'description', 'url',
    'has_dentalins', 'has_healthins', 'is_remote', 'has_401k', 'salary_range',
    'part_time_permitted', 'date_active', 'date_inactive', 'last_processed'
], defaults=(None,) * 15)
Page = namedtuple('Page', ['jobs', 'paging'])
ScrapResult = namedtuple('ScrapResult', ['company', 'job', 'scraper'])

@dataclass
class Stats:
    created: int = 0
    failed: int = 0
    ignored: int = 0
    updated: int = 0

    def __add__(self, other):
        return Stats(
            created=self.created + other.created,
            failed=self.failed + other.failed,
            ignored=self.ignored + other.ignored,
            updated=self.updated + other.updated,
        )

    def __str__(self):
        return self.format(self)

    @staticmethod
    def format(stat):
        return (
            "created: {stat.created} / updated: {stat.updated} /" +
            "ignored: {stat.ignored} / failed: {stat.failed}"
        ).format(stat=stat)



class SiteScraper:
    """Scraps a site to collect all job listings.
    """

    def get_locations(self, location_names: List[str]) -> List[Location]:
        """Retrives locations matching provided names.

        :param location_names: names of locations to retrieve
        :type location_names: List[str]
        :return: locations matching provided names.
        :rtype: List[Location]
        """
        if location_names:
            return Location.objects.filter(name__in=location_names)
        return []

    def scrape_vacancies(self) -> List[Job]:
        raise NotImplementedError()

    def scrap_vacancy_details(self, company: Company, job: Job):
        raise NotImplementedError()


class WorldBankGroupScraper(SiteScraper):
    """Scraper for the World Bank Group careers page.
    """
    ID = 'world-bank-group'
    VIEW_FIELDS = ['__VIEWSTATE', '__VIEWSTATEGENERATOR']
    FORM_DATA = {
        '__ASYNCPOST': True,
        '__EVENTTARGET': 'ctl00$siteContent$widgetLayout$rptWidgets$ctl03$widgetContainer$ctl00$btnSearch',
        'ctl00$ScriptManager': 'ctl00$siteContent$widgetLayout$rptWidgets$ctl03$widgetContainer$ctl00$ctl00|ctl00$siteContent$widgetLayout$rptWidgets$ctl03$widgetContainer$ctl00$btnSearch',
        'ctl00$siteContent$widgetLayout$rptWidgets$ctl03$widgetContainer$ctl00$rptCustomFields$ctl03$customFieldWrapper$ctl00$selectOu$itemName':'',
        'ctl00$siteContent$widgetLayout$rptWidgets$ctl03$widgetContainer$ctl00$rptCustomFields$ctl03$customFieldWrapper$ctl00$selectOu$itemId': 0,
    }

    def __init__(self, url: str):
        self.url = url
        self.form_state = {}
        self.session = HTMLSession()

    def get_pagination_details(self, page: Element) -> List[Dict[str, str]]:
        """Returns paging details within a html page.

        :param page: html page to process to extract paging details
        :type page: Element
        :return: list of paging details
        :rtype: List[Dict[str, str]]
        """
        links = []
        paging = page.find('div.results-paging', first=True)

        spans = [] if not paging else paging.find('.pagerLink')
        for span in spans:
            links.append({
                'page_no': span.text,
                'event_target': span.attrs.get('id').replace('_', '$')
            })

        return links

    def get_jobs(self, page: Element, page_no: str) -> List[Job]:
        """Returns job postings within a html page.

        :param page: html page to process to extract jobs.
        :type page: Element
        :param page_no: the page number being processes
        :type page_no: str
        :return: list of jobs
        :rtype: List[Job]
        """
        jobs: List[Job] = []
        table = page.find('table#tableResults', first=True)

        rows = [] if not table else table.find('tr')
        for row in rows:
            cells = row.find('td')
            if not cells:
                continue

            text = '::'.join([c.text for c in cells])
            text_hash = hashlib.sha256(text.encode('utf-8'))

            jobs.append(Job(**{
                'page_no': page_no,
                'hash': text_hash.hexdigest(),
                'data': {
                    'title': cells[0].text.replace('\xa0', ' '),
                    'href': cells[0].find('a', first=True).attrs['href'],
                    'location': cells[1].text,
                    'job-family': cells[2].text,
                    'deadline': cells[3].text
                }
            }))

        return jobs

    def _update_state(self, res: HTMLResponse) -> None:
        self.form_state.clear()

        find_input = lambda f: res.html.find(f'input[name={f}]', first=True)
        elems = {f: find_input(f) for f in self.VIEW_FIELDS}
        self.form_state.update({
            f: elem.attrs.get('value') for (f, elem) in elems.items()
        })

    def _get_page(self, page_no: str = '1', event_target: str = None) -> Page:
        log.debug(f'processing page {page_no} ...')
        data = {**self.FORM_DATA, **self.form_state}
        if event_target:
            data.update({
                '__EVENTTARGET': event_target,
                'ctl00$ScriptManager': event_target
            })

        res = self.session.post(self.url, data=data)
        res.raise_for_status()
        self._update_state(res)

        return Page(
            jobs=self.get_jobs(res.html, page_no),
            paging=self.get_pagination_details(res.html)
        )

    def scrape_vacancies(self) -> List[Job]:
        log.debug(f'processing page: {self.url} ...')
        res = self.session.get(self.url)
        res.raise_for_status()
        self._update_state(res)

        (jobs, paging) = self._get_page()
        for page_info in paging[1:]:
            time.sleep(15)
            page = self._get_page(**page_info)
            jobs.extend(page.jobs)

        log.debug(f'{len(jobs)} job(s) extracted ...')
        return jobs

    def scrap_vacancy_details(self, company: Company, job: Job) -> JobDetail:
        session = HTMLSession()
        job_url = urljoin(self.url, job.data['href'])
        res = session.get(job_url)
        res.raise_for_status()

        # extract page contents
        content = res.html.find('.cs-atscs-jobdet-rtpane', first=True)
        info, desc = content.find('table')
        title = content.find('p > span', first=True).text

        rows = [[td.text for td in tr.find('td')] for tr in info.find('tr')]
        role_title = f'{title} | {rows[1][1]} | {rows[0][1]}'

        locations = []
        if len(rows) >= 7:
            location_names = [name.strip() for name in rows[6][1].split(';')]
            locations = self.get_locations(location_names)

        return  JobDetail(
            entry_hash=job.hash,
            company=company,
            date_active=datetime.today(),
            description=desc.text,
            locations=locations,
            role_title=role_title,
            url=job_url,
        )


class Engine:
    """Engine to coordinate scraping activities.
    """
    scrapers = {
        WorldBankGroupScraper.ID: WorldBankGroupScraper
    }

    stats = {
        WorldBankGroupScraper.ID: Stats(created=0, failed=0, updated=0, ignored=0)
    }

    def __init__(self, companies: List[Company]):
        """Initializes a new engine object.

        :param scrapers: list of companies to scrap jobs from
        :type scrapers: List[Company]
        """
        self.companies = companies
        self.known_openings = {}

    def scrape_vacancies(self) -> Iterable[ScrapResult]:
        """Returns jobs scraped from vacancies urls for companies added to engine.
        """
        # find scrapable companies
        scrapable = [c for c in self.companies if c.name_slug in self.scrapers]
        label = 'company' if len(scrapable) == 1 else 'companies'
        log.debug(f'{len(scrapable)} {label} to be scraped ...')

        for company in scrapable:
            log.debug(f'Scraping vacancies for {company.name} ...')

            scraper_cls = self.scrapers[company.name_slug]
            scraper = scraper_cls(company.vacancies_url)
            for job in scraper.scrape_vacancies():
                yield ScrapResult(company, job, scraper)

    def process_vacancy(self, result: ScrapResult):
        # scrap job details
        (company, job, scraper) = result
        job_detail = scraper.scrap_vacancy_details(company, job)
        stat = self.stats[company.name_slug]

        if result.job.hash in self.known_openings:
            opening = Opening.objects.filter(entry_hash=result.job.hash).first()
            self.known_openings[result.job.hash].update({ 'active': True })

            # check if job is to be updated
            if not opening.is_match({ 'job': job_detail._asdict() }):
                log.debug('Updating existing job ...')
                opening.description = job_detail.description
                opening.save()
                stat.updated += 1
                return

            stat.ignored += 1
            return

        # persist new job
        log.debug('Saving new job ...')
        data = job_detail._asdict()
        locations = data.pop('locations')

        opening = Opening(**data)
        if locations:
            opening.locations.add(*locations)

        opening.save()
        stat.created += 1

    def _display_stats(self):
        """Display stats for the scraping operation.
        """
        # display stats for each company
        for (id, stat) in self.stats.items():
            log.debug(f"Stats ({id}) :: {stat}")

        # display total status
        total = reduce(lambda acc, item: acc + item, self.stats.values())
        log.debug(f"Total :: {total}")

    def _update_inactive_openings(self):
        # idenfy known openings that are no longer active
        inactive_openings = list(filter(
            lambda value: 'active' not in value,
            self.known_openings.values()
        ))

        log.debug(f'{len(self.known_openings)} active known openings ...')
        if inactive_openings:
            log.debug(f'{len(inactive_openings)} openings have gone inactive ...')
            with connection.cursor() as cursor:
                dml = "UPDATE jobs_openings SET date_inactive={0} WHERE id in ({1})"
                cursor.execute(dml.format(
                    datetime.today().date().isoformat(),
                    ', '.join([o['id'] for o in inactive_openings])
                ))

    def _after_scrape(self):
        """Performs a series of operations after the scrapping operation.
        """
        try:
            self._update_inactive_openings()
            self._display_stats()
        except Exception as ex:
            log.error(f"After scrape operation failed. Error: {ex}")

    def _before_scrape(self):
        """Performs a series of operation before the actual scrapping begins.
        """
        # compile hash of all known active openings
        try:
            fields = ('id', 'entry_hash')
            openings = Opening.objects.filter(date_inactive__isnull=True).values(*fields)
            for opening in openings:
                self.known_openings.update({
                    opening['entry_hash']: {'id': opening['id']}
                })

            log.debug(f'{len(opening)} known active openings found ...')
        except Exception as ex:
            log.error(f'Before scrape operation failed. Error: {ex}')

    def execute(self):
        """Initiates jobs scraping for added companies.
        """
        start_time = datetime.now()
        log.info(f"Scraping started ... at {start_time.strftime('%H:%M')}")
        self._before_scrape()

        try:
            for result in self.scrape_vacancies():
                try:
                    time.sleep(10)
                    self.process_vacancy(result)
                    time.sleep(10)
                except Exception as ex:
                    log.error(ex)
                    stat = self.stats[result.company.name_slug]
                    stat.failed += 1

            finish_time = datetime.now()
            op = 'finished'
        except Exception as ex:
            log.error(ex)
            finish_time = datetime.now()
            op = 'aborted'

        self._after_scrape()
        log.info(
            f"Scraping {op} at {finish_time.strftime('%H:%M')} " +
            f"(duration: {str(finish_time - start_time)})"
        )
