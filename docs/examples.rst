.. _basin3dexamples:

Examples
********

Read more in the `Django tutorial <https://docs.djangoproject.com/en/4.0/intro/tutorial01/>`_ for creating an Django app. Change the tutorial version to match the Django version you are using.

Example BASIN-3D broker connecting to USGS data source
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In this example, you will create an example BASIN-3D broker and connect to
the USGS Daily and Instantaneous Values service. The plugin to this USGS
publicly-available data source is bundled with core synthesis code in basin3d.

1. Create a virtual environment with a supported python version and activate it.
2. Install django-basin3d::

    $ pip install django-basin3d

3. Start a Django app::

    $ django-admin startproject mybroker

A new directory will be created called mybroker that contains a subdirectory called mybroker and manage.py.

4. Change directories::

    $ cd mybroker/mybroker

5. Configure the plugins.

First, create the plugins directory::

    $ mkdir plugins

Then, create ./plugins/__init__.py file with the following code:

.. code-block::

    from basin3d.plugins import usgs

    __all__ = ['usgs']

This ./plugins/__init__.py file configures the USGS plugin bundled with basin3d.

6. Modify the settings.py file as follows.

Add the following line of code as the first line in the file::

    from __future__ import print_function

Add the first three lines below to the INSTALLED_APPS section.

.. code-block::

    INSTALLED_APPS = [
        'mybroker',
        'rest_framework',
        'django_basin3d',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
    ]

Add the following code to the end of settings.py file.

.. code-block::

    import os

    STATIC_ROOT = os.path.join(BASE_DIR, "static/")

    REST_FRAMEWORK = {
        # Use Django's standard `django.contrib.auth` permissions,
        # or allow read-only access for unauthenticated users.
        'DEFAULT_PERMISSION_CLASSES': [
            #'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
        ],
        'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.AcceptHeaderVersioning',
        'DEFAULT_VERSION': '1.0',
        'ALLOWED_VERSIONS': ['1.0'],
        'TEST_REQUEST_DEFAULT_FORMAT': 'json',
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework.authentication.SessionAuthentication',
        ),
    }

    BASIN3D = {
    }

7. Create an apps.py module with the following code.

.. code-block::

    from __future__ import unicode_literals

    from django.apps import AppConfig


    class MyBrokerConfig(AppConfig):
        name = 'mybroker'

8. Modify the urls.py module to be the following:

.. code-block::

    from django.contrib import admin
    from django.urls import include, re_path

    from django_basin3d import urls as b3durls

    admin.autodiscover()

    # Wire up our API using automatic URL routing.
    # Additionally, we include login URLs for the browsable API.
    urlpatterns = [
        re_path(r'^', include(b3durls)),
        re_path(r'^admin/', admin.site.urls),
        re_path(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
    ]

9. Migrate the django-basin3d database::

    $ cd ..
    $ python manage.py migrate

10. Start the application::

    $ python manage.py runserver

11. Open the app in a browser with the url: http://127.0.0.1:8000/

The Broker API root view will be rendered with the following index.

.. code-block::

    {
        "datasource": "http://127.0.0.1:8000/datasource/",
        "attributemapping": "http://127.0.0.1:8000/attributemapping/",
        "observedproperty": "http://127.0.0.1:8000/observedproperty/",
        "measurementtvptimeseries": "http://127.0.0.1:8000/measurement_tvp_timeseries/",
        "monitoringfeature": "http://127.0.0.1:8000/monitoringfeature/"
    }

12. Confirm that the connection to USGS is working using the following queries.

View the USGS datasource:
http://127.0.0.1:8000/datasource/

.. code-block::

    [
        {
            "url": "http://127.0.0.1:8000/datasource/USGS/",
            "name": "USGS",
            "location": "https://waterservices.usgs.gov/nwis/",
            "id_prefix": "USGS",
            "attribute_mapping": "http://127.0.0.1:8000/datasource/USGS/attribute_mapping/",
            "observed_property": "http://127.0.0.1:8000/datasource/USGS/observed_property/",
            "check": "http://127.0.0.1:8000/datasource/USGS/check/"
        }
    ]

View the USGS monitoring feature regions:
http://127.0.0.1:8000/monitoringfeature/regions/

.. code-block::

    {
        "query": {
            "feature_type": "REGION"
        },
        "data": [
            {
                "id": "USGS-01",
                "name": "New England",
                "description": "REGION: New England",
                "feature_type": "REGION",
                "observed_properties": [],
                "related_sampling_feature_complex": [],
                "shape": "SURFACE",
                "coordinates": null,
                "description_reference": null,
                "related_party": [],
                "utc_offset": null,
                "url": "http://127.0.0.1:8000/monitoringfeature/regions/USGS-01/"
            },
            ...
        ]
    }

Try a query of USGS point monitoring features for a specific subbasin:
http://127.0.0.1:8000/monitoringfeature/points/?datasource=USGS&parent_feature=USGS-14020001

.. code-block::

    {
        "query": {
            "datasource": [
                "USGS"
            ],
            "feature_type": "POINT",
            "parent_feature": [
                "USGS-14020001"
            ]
        },
        "data": [
            {
            "id": "USGS-09106800",
            "name": "TAYLOR RIVER ABOVE TRAIL CREEK NR TAYLOR PARK, CO",
            "description": null,
            "feature_type": "POINT",
            "observed_properties": [],
            "related_sampling_feature_complex": [
                {
                    "related_sampling_feature": "USGS-14020001",
                    "related_sampling_feature_type": "SUBBASIN",
                    "role": "PARENT",
                    "url": "http://127.0.0.1:8000/monitoringfeature/subbasins/USGS-14020001/"
                }
            ],
            "shape": "POINT",
            "coordinates": {
                "absolute": {
                    "horizontal_position": [
                        {
                            "x": -106.6009444,
                            "y": 38.92469444,
                            "datum": "NAD83",
                            "type": "GEOGRAPHIC",
                            "latitude": 38.92469444,
                            "longitude": -106.6009444,
                            "units": "DD"
                        }
                    ],
                    "vertical_extent": [
                        {
                            "value": 9681.31,
                            "resolution": 0.14,
                            "distance_units": null,
                            "datum": "NAVD88",
                            "type": "ALTITUDE"
                        }
                    ]
                },
                "representative": null
            },
            "description_reference": null,
            "related_party": [],
            "utc_offset": null,
            "url": "http://127.0.0.1:8000/monitoringfeature/points/USGS-09106800/"
            },
            {
                "id": "USGS-09107000",
                "name": "TAYLOR RIVER AT TAYLOR PARK, CO.",
                "description": null,
                "feature_type": "POINT",
                "observed_properties": [
                    "RDC",
                    "SC",
                    "WT"
                ],
                "related_sampling_feature_complex": [
                    {
                        "related_sampling_feature": "USGS-14020001",
                        "related_sampling_feature_type": "SUBBASIN",
                        "role": "PARENT",
                        "url": "http://127.0.0.1:8000/monitoringfeature/subbasins/USGS-14020001/"
                    }
                ],
                "shape": "POINT",
                "coordinates": {
                    "absolute": {
                        "horizontal_position": [
                            {
                                "x": -106.5666966,
                                "y": 38.86027127,
                                "datum": "NAD83",
                                "type": "GEOGRAPHIC",
                                "latitude": 38.86027127,
                                "longitude": -106.5666966,
                                "units": "DD"
                            }
                        ],
                        "vertical_extent": [
                            {
                                "value": 9340.0,
                                "resolution": 10.0,
                                "distance_units": null,
                                "datum": "NGVD29",
                                "type": "ALTITUDE"
                            }
                        ]
                    },
                    "representative": null
                },
                "description_reference": null,
                "related_party": [],
                "utc_offset": null,
                "url": "http://127.0.0.1:8000/monitoringfeature/points/USGS-09107000/"
            },
            ...
        ]
    }

Try a USGS timeseries data query:
http://127.0.0.1:8000/measurement_tvp_timeseries/?monitoring_feature=USGS-09107000&observed_property=RDC&start_date=2000-01-01&end_date=2000-03-01

.. code-block::

    {
        "query": {
            "monitoring_feature": [
                "USGS-09107000"
            ],
            "observed_property": [
                "RDC"
            ],
            "start_date": "2000-01-01",
            "aggregation_duration": "DAY",
            "end_date": "2000-03-01"
        },
        "data": [
            {
                "aggregation_duration": "DAY",
                "time_reference_position": "MIDDLE",
                "statistic": "MEAN",
                "result": {
                    "value": [
                        [
                            "2000-01-01T00:00:00.000",
                            1.1043570329999999
                        ],
                        [
                            "2000-01-02T00:00:00.000",
                            1.076040186
                        ],
                        [
                            "2000-01-03T00:00:00.000",
                            1.047723339
                        ],
                        ...
                    ],
                    "result_quality" [
                        "VALIDATED",
                        "VALIDATED",
                        "VALIDATED"
                        ...
                    ]
                },
                "unit_of_measurement": "m^3/s",
                "datasource": "http://127.0.0.1:8000/datasource/USGS/"
                "id": "USGS-09107000",
                "type": "MEASUREMENT_TVP_TIMESERIES",
                "utc_offset": -7,
                "phenomenon_time": null,
                "observed_property": "RDC",
                "result_quality": [
                    "VALIDATED"
                ],
                "feature_of_interest": {
                    "id": "USGS-09107000",
                    "name": "TAYLOR RIVER AT TAYLOR PARK, CO.",
                    "description": null,
                    "feature_type": "POINT",
                    "observed_properties": [
                        "RDC",
                        "SC",
                        "WT"
                    ],
                    "related_sampling_feature_complex": [
                        {
                            "related_sampling_feature": "USGS-14020001",
                            "related_sampling_feature_type": "SUBBASIN",
                            "role": "PARENT",
                            "url": "http://127.0.0.1:8000/monitoringfeature/subbasins/USGS-14020001/"
                        }
                    ],
                    "shape": "POINT",
                    "coordinates": {
                        "absolute": {
                            "horizontal_position": [
                                {
                                    "x": -106.5666966,
                                    "y": 38.86027127,
                                    "datum": "NAD83",
                                    "type": "GEOGRAPHIC",
                                    "latitude": 38.86027127,
                                    "longitude": -106.5666966,
                                    "units": "DD"
                                }
                            ],
                            "vertical_extent": [
                                {
                                    "value": 9340.0,
                                    "resolution": 10.0,
                                    "distance_units": null,
                                    "datum": "NGVD29",
                                    "type": "ALTITUDE"
                                }
                            ]
                        },
                        "representative": null
                    },
                    "description_reference": null,
                    "related_party": [],
                    "utc_offset": null,
                    "url": "http://127.0.0.1:8000/monitoringfeature/points/USGS-09107000/",
                },
                "feature_of_interest_type": "POINT"
            }
        ]
    }
