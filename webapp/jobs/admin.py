from django.contrib import admin
from django.contrib.gis.admin import GeoModelAdmin

from .models import Company, Location, Opening


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    date_hierarchy = 'last_updated'
    list_display = (
        'name', 'industry', 'vacancies_url', 'last_updated', 'update_freq'
    )


@admin.register(Location)
class LocationAdmin(GeoModelAdmin):
    list_display = ('opening', 'name', 'geom')
    default_lat = 37.0902
    default_lon = 95.7129
    default_zoom = 3


@admin.register(Opening)
class OpeningAdmin(admin.ModelAdmin):
    list_display = ('company', 'role_title', 'url', 'is_remote', 'has_401k')
