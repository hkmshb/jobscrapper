"""Defines objects for handling data scraping.
"""

from typing import List
from jobs.models import Company


class SiteScraper:
    """Scraps a site to collect all job listings.
    """
    pass


class JobScrapTask:
    """Scraps the details for an individual job.
    """
    pass


class Engine:
    """Engine to coordinate scraping activities.
    """

    def __init__(self, companies: List[Company]):
        """Initializes a new engine object.

        :param scrapers: list of companies to scrap jobs from
        :type scrapers: List[Company]
        """
