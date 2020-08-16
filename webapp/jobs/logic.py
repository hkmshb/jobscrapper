"""Handles data validation around data persistence.
"""

from typing import Dict, List

from django.core.exceptions import ObjectDoesNotExist
from glom import glom

from .exceptions import JobsError, OpeningExistError
from .models import Company, Opening


def opening_insert(data: dict) -> Opening:
    """Inserts an opening into the database.

    :param data: job opening details
    :type data: dict
    """
    # check that opening with same url doesn't already exist
    job_url = glom(data, 'job.url')
    opening = Opening.objects.filter(url=job_url).first()
    if opening:
        raise OpeningExistError(job_url)

    job = glom(data, 'job')
    if 'company' not in job:
        job['company'] = glom(data, 'company')

    opening = Opening(**job)
    opening.save()

    return opening


def opening_update(opening: Opening, data: dict) -> Opening:
    """Updates details of an opening that exists within the database.

    :param opening: the current opening details
    :type opening: Opening
    :param data: the data to update opening with
    :type data: dict
    """
    if opening.url != glom(data, 'job.url'):
        raise JobsError('Opening job url cannot be changed')

    if opening.company.id != glom(data, 'company.id'):
        raise JobsError('Company for an opening cannot be changed')

    target_fields = [f for f in glom(data, 'job') if f not in ('id', 'company')]
    for field in target_fields:
        value = glom(data, f'job.{field}')
        setattr(opening, field, value)

    opening.save()
    return opening
