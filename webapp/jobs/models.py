import re
from enum import Enum

from django.db import models
from django.contrib.gis.db import models as gismodels
from django.contrib.postgres import fields as pgmodels
from django.contrib.postgres import search
from django.utils.text import slugify

from core.models import Entity


class DurationUnit(Enum):
    DAYS = 'days'
    HOURS = 'hours'

    @classmethod
    def values(cls):
        return [e.value for e in list(cls)]


class Company(Entity):
    """Defines fields for recording company details.
    """
    name = models.CharField(max_length=100, unique=True)
    name_slug = models.SlugField('Name Slug', max_length=100, unique=True)
    industry = models.CharField(max_length=100)
    vacancies_url = models.URLField('Vacancies Url', max_length=200)
    last_updated = models.DateTimeField('Last Updated', auto_now=False, auto_now_add=False)
    update_freq = models.IntegerField('Update Frequency', default=0)

    class Meta:
        verbose_name_plural = 'Companies'

    def save(self, *args, **kwargs):
        """Saves an instance of the model.
        """
        if not self.name_slug:
            self.name_slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        """Returns string representation of the model.
        """
        return self.name


class Location(Entity):
    """Defineds fields for recording opening location details.
    """
    name = models.CharField(max_length=100, unique=True)
    geom = gismodels.PointField('GPS Coord', null=True, blank=True)

    def __str__(self):
        """Returns string representation of the model.
        """
        return f'{self.name}'


class Opening(Entity):
    """Defines fields for recording job opening details.
    """
    entry_hash = models.CharField('Title Hash', max_length=200, unique=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    locations = models.ManyToManyField(Location, blank=True)
    role_title = models.CharField('Role Title', max_length=100)
    description = models.TextField()
    url = models.URLField('Job Url', max_length=200, unique=True)
    is_remote = models.NullBooleanField('Is Remote')
    part_time_permitted = models.NullBooleanField('Part-Time Permitted')
    has_401k = models.NullBooleanField('Has 401k')
    has_dentalins = models.NullBooleanField('Has Dental Insurance')
    has_healthins = models.NullBooleanField('Has Health Insurance')
    salary_range = pgmodels.IntegerRangeField('Salary Range', blank=True, null=True)
    date_active = models.DateField('Date Active', auto_now=False, auto_now_add=False)
    date_inactive = models.DateField(
        'Date Inactive', auto_now=False, auto_now_add=False, blank=True, null=True
    )
    date_created = models.DateTimeField('Date Created', auto_now=False, auto_now_add=True)
    tsdocument = search.SearchVectorField('Document')

    def is_match(self, data: dict):
        """Returns True if data matches opening details otherwise False.

        :param data: details to match against this opening instance.
        :type data: dict
        """
        pattern = re.compile('date_*')
        exclude_list = (
            'id', 'company', 'locations', 'entry_hash', 'tsdocument'
        )

        field_names = list(filter(
            lambda f: f not in exclude_list and not pattern.match(f),
            [f.name for f in self._meta.get_fields()]
        ))

        for field in field_names:
            if (
                field in data['job'] and
                hasattr(self, field) and
                getattr(self, field) != data['job'][field]
            ):
                return False

        return True

    def __str__(self):
        """Returns string representation of the model.
        """
        return f'{self.role_title} at {self.company.name}'
