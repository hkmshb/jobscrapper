from django.http import HttpRequest
from django.db import models
from django.shortcuts import render, get_object_or_404

from jobs.models import Opening


def opening_list(request: HttpRequest):
    openings = Opening.objects.all()
    return render(request, 'jobs/list.html', {
        'openings': openings
    })


def opening_show(request: HttpRequest, opening_id: int):
    opening = get_object_or_404(Opening, pk=opening_id)

    data = []
    for field in opening._meta.get_fields():
        if field.name in ('id', 'location', 'role_title'):
            continue

        value = field.value_from_object(opening)
        is_url = isinstance(field, models.URLField)
        if isinstance(field, models.ForeignKey):
            try:
                model = field.related_model
                obj = model.objects.get(pk=value)
                value = str(obj)
            except Exception:
                pass

        data.append([ field, value, is_url ])

    return render(request, 'jobs/item.html', {
        'opening': opening,
        'data': data
    })
