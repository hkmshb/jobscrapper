.. _api:

API Reference
=============

.. module:: webapp

This part of the documentation covers all the interfaces of the Jobs Scraper. For parts where
the scraper depends on external libraries, the most important parts are document right here
with links to their respective canonical documentation.

Main Interfaces
---------------

All of the scraper's functionality are provided within two Django applications (:py:mod:`core`
and :py:mod:`jobs`) within the :py:mod:`webapp` Django project.

.. autoclass:: jobs.scraper.SiteScraper
.. autoclass:: jobs.scraper.SequoiaScraper
.. autoclass:: jobs.scraper.WorldBankGroupScraper
.. autoclass:: jobs.scraper.Engine


Other Interfaces
----------------

webapp.core
~~~~~~~~~~~

Admin
*****

.. autoclass:: core.admin.DocumentAdmin
.. autoclass:: core.admin.DescriptionAdmin

Forms
*****

.. autoclass:: core.forms.SimpleSignupForm

Models
******

.. autoclass:: core.models.User
.. autoclass:: core.models.Entity
.. autoclass:: core.models.Description
.. autoclass:: core.models.Document


webapp.jobs
~~~~~~~~~~~

Admin
*****

.. autoclass:: jobs.admin.CompanyAdmin
.. autoclass:: jobs.admin.LocationAdmin
.. autoclass:: jobs.admin.OpeningAdmin

Exceptions
**********

.. autoexception:: jobs.exceptions.JobsError
.. autoexception:: jobs.exceptions.OpeningExistError


Forms
*****

.. autoclass:: jobs.forms.PagingForm
.. autoclass:: jobs.forms.SearchForm

Models
******

.. autoclass:: jobs.models.DurationUnit
.. autoclass:: jobs.models.Company
.. autoclass:: jobs.models.Location
.. autoclass:: jobs.models.Opening
