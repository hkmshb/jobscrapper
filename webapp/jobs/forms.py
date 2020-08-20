from urllib.parse import urlencode

from django import forms
from django.db import models
from jobs.models import Location


class PagingForm(forms.Form):
    page = forms.IntegerField(required=False, min_value=1)
    page_size = forms.IntegerField(required=False)


class SearchForm(PagingForm):
    q = forms.CharField(required=False, max_length=100, strip=True)
    is_spatial = forms.BooleanField(required=False, initial=False)
    location = forms.ModelChoiceField(
        empty_label="(Select Location)",
        required=False,
        queryset=Location.objects.order_by('name').all()
    )

    def urlencode(self):
        def get(value):
            if not isinstance(value, models.Model):
                return str(value)

            return getattr(value, 'id')

        data = {
            key: get(value)
            for key, value in self.clean().items()
            if value and key != 'page'
        }
        return urlencode(data)
