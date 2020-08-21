# CHANGE LOG

## 2020.08.21

- Added `core` app with custom user and some other models
- Refactored entire migrations for the application
  - move superuser creation migration from the `jobs` app to the new `core` app
  - add trigger creation migration which auto-updates the column which supports FTS on the app
- Added `django.contrib.postgres` and `django.contrib.gis` to `INSTALLED_APPS` to use models
  that support storing and managing spatial data
- Extended `views.py` to implement both FTS-based and spatial-based search
- Added static resources `bulma.min.css`, `bulma-switch.min.css` and `nanojs.min.js` used within
  the list and details view for openings.
- Added more columns the openings table displayed on the landing page

## 2020.08.17

- Updated `Company` and `Opening` models
  - `Company` updates: added `name_slug` field, changed `last_updated` to a datetime field
  - `Opening` update: made `url` field unique, then `salary_range` and `date_inactive` to
    be nullable; added `date_created` and `last_processed` datetime fields
- Added fixtures and unit tests
- Added logic for handling opening insertion and update
- Added `scrapejobs` custom command
- Added views for listing openings and showing details for a single opening
- Added `entrypoint.sh` script to ease running custom commands within the webapp container

## 2020.08.13

- Replaced the `polls` Django app with `jobs`
- Changed database engine to `django.contrib.gis.db.backends.postgis` within `settings.py` as this is
  required to use GeoDjango models.
- Introduced `django-dotenv` to ease working with `.env` file directly on the host system thus eliminating
  the need for a separate `.env.sh` file.
- Added environment variables for configuring parameters for creatiing the Django `superuser`. Find the
  variables (with `DJAPP_SU_*` prefix) within `.env.template`.
  > The `superuser` creation is done within a migration script to ensure it's only ever executed once
- Updated `./scripts/start.sh` script to run migrations just before starting the application.
- Updated `Dockerfile` to match `Dockerfile.pipenv` with the base image changed from **Alpine** Linux to
  **Debian** Linux and necessary commands updated; `Dockerfile.pipenv` was deleted afterwards.
  > The Alpine base image was changed as a successful install of GDAL on could not be accomplished.
