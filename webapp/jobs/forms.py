from urllib.parse import urlencode

from django import forms
from django.db import models
from django.core.exceptions import ValidationError

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
            for key, value in self.cleaned_data.items()
            if value is not None and get(value) and key != 'page'
        }
        return urlencode(data)

    def clean(self):
        data = super().clean()
        is_spatial = data.get('is_spatial') or False
        location = data.get('location') or None
        q = data.get('q') or None

        if is_spatial:
            if not location:
                self.add_error('location', 'Field is required')

            # ensure q is numberic
            if q and not q.isnumeric():
                self.add_error('q', 'Numeric value expected')

        return  data
