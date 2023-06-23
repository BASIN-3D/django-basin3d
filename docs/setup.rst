=====
Setup
=====

Django BASIN-3D is a Django app that acts as a Broker for Assimilation, Synthesis and Integration of eNvironmental
Diverse, Distributed Datasets.

The setup instructions below assume familiarity with Django. For more details, see https://www.djangoproject.com/start/

Custom plugins are developed for a broker instance. See ~/example-django/ directory containing the app "mybroker"
for a broker instance example with datasource "Alpha" at https://github.com/BASIN-3D/django-basin3d.

Install
-------

If you haven't created a Django project for your custom broker, create one. See https://www.djangoproject.com/start/
for details. Once the custom Django broker project is created, install the BASIN-3D source distribution to
Python environment for your Django project.

Install a source distribution with pip::

    $ pip install django-basin3d

Make sure your installation was successful::

    $ python
    >>> import django_basin3d
    >>>

Django Settings
---------------

In the Django settings, add "django_basin3d" and its dependencies to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
    '<your app>',
    'rest_framework',
    'django_basin3d',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles'

]


URLConf
-------

Include the basin3d URLconf in your project urls.py like this::

    from django.conf.urls import include, url
    from django_basin3d import urls as db_urls

    url(r'^', include('db_urls.urls')),

See ~/example-django/mybroker/urls.py for an example.

Implement Data Source plugins
-----------------------------

Create one or more plugins in a plugins module in `your-app/plugins.py`. The following files
must be placed in `your-app/` directory along side `plugins.py`

`basin3d_observed_property_vocabulary.csv`
..........................................
Hydrology variables have been defined in `basin3d`.  These  broker variables are in a comma separated values (csv)
file named `basin3d_observed_property_vocabulary.csv`_ and can be found at https://github.com/BASIN-3D/basin3d.

.. _basin3d_observed_property_vocabulary: https://github.com/BASIN-3D/basin3d/blob/main/basin3d/data/basin3d_observed_property_vocabulary.csv


`<plugin_name>_mapping.csv`
...........................
Map your measurement variables for your plugin variables. The name of the file should be
`<plugin_name>_mapping.csv`. This file must be placed this in `your-app/` directory
(e.g `your-app/alpha_mapping.csv`) .

.. literalinclude:: ../example-django/mybroker/alpha_mapping.csv


Extend the broker source plugin with the described attributes. The following example is from ~example-django/mybroker/plugins.py.

.. literalinclude:: ../example-django/mybroker/plugins.py
   :language: python


Migrate the App
---------------

Run `python manage.py migrate` to create the Django BASIN-3d models. This will create the database and load the app's
plugins.


Run the Server
--------------

Start the development server::

    $ bin/python manage.py runserver

Visit http://127.0.0.1:8000/ to view the REST API.

Visit http://127.0.0.1:8000/admin/ to manage a BASIN-3D models (you'll need the Admin app
enabled in the project's urls.py)::

    url(r'^admin/', include(admin.site.urls)),

To create an admin user::

    ./manage.py createsuperuser

To exit running the server, control + C.

