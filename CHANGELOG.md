# CHANGE LOG

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
