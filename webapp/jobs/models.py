import uuid
from django.db import models
from django.contrib.gis.db import models as gismodels
from django.contrib.postgres import fields as pgmodels


class Entity(models.Model):
    """Abstract base models for all models in the application. Defines common attribute
    used in all models in the application.
    """
    id = models.BigAutoField(primary_key=True)

    class Meta:
        abstract = True


class Company(Entity):
    """Defines fields for recording company details.
    """
    name = models.CharField(max_length=100, unique=True)
    industry = models.CharField(max_length=100)
    vacancies_url = models.URLField(max_length=200)
    last_updated = models.DateField(auto_now=False, auto_now_add=False)
    update_freq = models.IntegerField('Update frequency (in days)', default=0)


class Opening(Entity):
    """Defines fields for recording job opening details.
    """
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    role_title = models.CharField(max_length=50)
    description = models.TextField()
    url = models.URLField(max_length=200)
    is_remote = models.NullBooleanField()
    part_time_permitted = models.NullBooleanField()
    has_401k = models.NullBooleanField()
    has_dentalins = models.NullBooleanField()
    has_healthins = models.NullBooleanField()
    salary_range = pgmodels.IntegerRangeField()
    date_active = models.DateField(auto_now=False, auto_now_add=False)
    date_inactive = models.DateField(auto_now=False, auto_now_add=False)


class Location(Entity):
    """Defineds fields for recording opening location details.
    """
    opening = models.ForeignKey(Opening, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    geom = gismodels.PointField()
