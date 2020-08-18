from django.core.paginator import Paginator
from django.db import models
from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404

from jobs.models import Opening

PAGE_SIZE = 25


def opening_list(request: HttpRequest):
    """Renders page listing openings.

    :param request: HTTP request object
    :type request: HttpRequest
    """
    page_no = request.GET.get('page', 1)
    page_sz = request.GET.get('page_size', PAGE_SIZE)
    search_term = request.GET.get('q')

    # handle search term
    if search_term:
        openings = Opening.objects.filter(tsdocument=search_term)
    else:
        openings = Opening.objects.all()

    openings = openings.order_by('id')
    p = Paginator(openings, page_sz)
    page = p.get_page(page_no)

    # update querystring
    qs = request.GET.copy()
    if 'page' in qs:
        del qs['page']

    if 'q' in qs and not search_term:
        del qs['q']

    return render(request, 'jobs/list.html', {
        'openings': page,
        'q': search_term,
        'qs': qs,
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
