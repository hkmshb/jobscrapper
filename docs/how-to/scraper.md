# Scraper

The main functionalities of the `Jobs Scraper` Django web application are provided within the
`jobs.scraper` python module.  

The scraping mechanism revolves around the `jobs.scraper.Engine` and `jobs.scraper.SiteScraper`
classes. The later defines the interface required of objects responsible for the actual scraping
of data from a specific website, while the later serves the general purpose of coordinating data
scraping activities from multiple sites using registered "SiteScrapers", besides also providing
an entry point to initiating data scraping.

## Running the Engine

The application provides a custom management command within `jobs.management.commands.scrapejobs`
which like other Django management commands can be executed directly from the cli. This custom
command provides a number of cli arguments and options which configure the exact operating
behaviour of the `jobs.scraper.Engine` to determine the:

- frequency of scraping of particular websites, and
- target job/opening listing websites to scrape

The code snippet below shows a skeletal outline of how the custom command operates:

```py
# read all db records of companies registered within the application
companies = Company.objects.filter(query)
...

# determine companies to be scraped; if update frequency is not to
# be ignore, read companies are filtered based on the `freq_unit`
# criteria to determine companies that have exceeded the set wait-
# time between scrapings...
ignore_update_freq = options['ignore_update_freq']
if not ignore_update_freq:
    freq_unit = DurationUnit(option['freq_unit'])
    moment = timezone.now()

    companies = list(filter(
      lambda c: self.allow_scaping(c, moment, freq_unit),
      companies
    ))

...

# run scraping engine for identified companies
engine = Engine(companies)
engine.execute()
```

## Available Scrapers

Derived classes of `jobs.scraper.SiteScraper` that provided targeted scraping of specific data
are:

- `jobs.scraper.SequoiaScraper`  
Scrapes listings at [https://www.sequoiacap.com/jobs](https://www.sequoiacap.com/jobs)

- .

- `jobs.scraper.WorldBankGroupScraper`  
Scrapes listings at [https://worldbankgroup.csod.com/ats/careersite/search.aspx](
https://worldbankgroup.csod.com/ats/careersite/search.aspx)

## Adding a new Scraper

The snippet below provides a guide to creating and registering a new Scraper.

```py
# Step One:
# Create a new scraper by defining a new class that derives from
# `jobs.scraper.SiteScraper`. See `jobs.scraper.SequoiaScraper`
# for a sample implementation.

class NewScraper(SiteScraper):

    ID = 'new-scraper'  # unique identifier for the scraper

    def scrape_vacancies(self) -> List[Job]:
        # this method should read and process the job/opening listings
        # page and identify individual entries in addition to handling
        # pagination through available pages if any
        ...

    def scrape_vacancy_details(self, company: Company, job: Job):
        # this method should handle the processing and extraction of
        # the full details from individual job/opening entries
        ...


# Step Two:
# Register created scraper with the `jobs.scraper.Engine`. Update
# the `Engine.scrapers` dictionary to include the new scraper...

class Engine:
    """Engine to coordinate scraping activities.
    """
    scrapers = {
        WorldBankGroupScraper.ID: WorldBankGroupScraper,
        SequoiaScraper.ID: SequoiaScraper,
        NewScraper.ID: NewScraper
    }

    ...
```

**NOTE:** The `Engine` is responsible for persisting extracted job/opening entries to the
database. Derived classes of `SiteScraper` should not be concerned nor attempt to handle
data persistence but rather focus solely on reading, processing and extract data from a
listing page.
