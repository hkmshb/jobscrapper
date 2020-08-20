from django.contrib.gis.measure import D
from django.core.paginator import Paginator
from django.db import models
from django.http import HttpRequest, QueryDict
from django.shortcuts import render, get_object_or_404

from jobs.forms import SearchForm
from jobs.models import Opening, Location


PAGE_SIZE = 25

def opening_list(request: HttpRequest):
    """Renders page listing openings.

    :param request: HTTP request object
    :type request: HttpRequest
    """
    form = SearchForm(request.GET)
    if not form.is_valid():
        return render(request, 'jobs/list.html', { 'form': form })

    data = form.clean()
    locations = []  # matched locations from spatial search

    q = data.get('q')
    is_spatial = data.get('is_spatial') or False

    openings = Opening.objects.all()
    if not is_spatial:
        # perform full-text search if term provided
        if q:
            openings = openings.filter(tsdocument=q)
    else:
        location = data.get('location')
        if not q:
            locations = [location]
        else:
            locations = Location.objects.filter(
                geom__distance_lte=(location.geom, D(mi=int(q)))
            )

        # filter openings by locations
        openings = openings.filter(locations__in=locations).distinct()

    # paginate results
    openings = openings.order_by('id')
    p = Paginator(openings, data.get('page_size') or PAGE_SIZE)
    page = p.get_page(data.get('page') or 1)

    # extract and return set query string values
    return render(request, 'jobs/list.html', {
        'locations': locations,
        'openings': page,
        'form': form
    })


def opening_show(request: HttpRequest, opening_id: int):
    """Renders the details page for an opening

    :param request: HTTP request object
    :type request: HttpRequest
    :param opening_id: the opening id
    :type opening_id: int
    """
    opening = get_object_or_404(Opening, pk=opening_id)
    exclude_list = ('id', 'role_title', 'tsdocument')

    data = []
    for field in opening._meta.get_fields():
        if field.name in exclude_list:
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
        elif isinstance(field, models.ManyToManyField):
            try:
                labels = [str(x) for x in value]
                value = '; '.join(labels)
            except Exception:
                pass

        data.append([ field, value, is_url ])

    return render(request, 'jobs/item.html', {
        'opening': opening,
        'data': data
    })
