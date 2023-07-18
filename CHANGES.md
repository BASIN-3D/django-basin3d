# Django BASIN-3D Releases

## Version 1.0.2
Updates DataSourceModelViewset.retrieve method to use plugin get method.

## Version 1.0.1
Minor maintenance to pin package versions.

## Version 1.0.0
This release updates django-basin3d to work with the latest basin3d v0.4.0 that enables complex- and multi-mappings between datasource vocabulary and BASIN-3D vocabulary.

Loggers are also now available in relevant modules. Logging can be configured in settings.py (See Django documentation).

** This is a breaking change. The django-basin3d migrations must be migrated from scratch. **

One approach is to delete the app's database. For the example-django app,

    $ cd example-django
    $ rm db.sqlite3

Then from the app's home directory (e.g., example-django), run the following:

    $ ./manage.py makemigrations
    $ ./manage.py migrate

## Version 0.1.0 (Alpha)
First alpha release of django-basin3d. Includes modernization of build system to publish to pypi.

django-basin3d requires basin3d, which performs core synthesis functionality. django-basin3d is the web framework portion of the original BASIN-3D codebase. We separated the web framework from the core synthesis functionality for improved maintenance and extensibility.
