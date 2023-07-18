import json

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class TestAPIRoot(TestCase):
    """
    Test the broker root API
    """

    def setUp(self):
        self.client = APIClient()

    def test_get(self):
        response = self.client.get('/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content.decode('utf-8')),
                         {
                             "datasource": "http://testserver/datasource/",
                             "attributemapping": "http://testserver/attributemapping/",
                             "observedproperty": "http://testserver/observedproperty/",
                             "measurementtvptimeseries": "http://testserver/measurement_tvp_timeseries/",
                             "monitoringfeature": "http://testserver/monitoringfeature/"
                         })


class TestSiteAPI(TestCase):
    """
    Test /monitoringfeature/<feature_type> api
    """

    def setUp(self):
        self.client = APIClient()

    def test_get_for_monitoring_feature_list(self):
        self.maxDiff = None
        response = self.client.get('/monitoringfeature/points/?datasource=A', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content.decode('utf-8')),
                         {
                             "query": {
                                 "datasource": [
                                     "A"
                                 ],
                                 "feature_type": "POINT"
                             },
                             "data": [
                                 {
                                     "id": "A-1",
                                     "name": "Point Location 1",
                                     "description": "The first point.",
                                     "feature_type": "POINT",
                                     "observed_properties": [
                                         "ACT",
                                         "Ag"
                                     ],
                                     "related_sampling_feature_complex": [
                                         {
                                             "related_sampling_feature": "A-Region1",
                                             "related_sampling_feature_type": "REGION",
                                             "role": "PARENT",
                                             "url": "http://testserver/monitoringfeature/regions/A-Region1/"
                                         }
                                     ],
                                     "shape": "POINT",
                                     "coordinates": {
                                         "absolute": {
                                             "horizontal_position": [
                                                 {
                                                     "x": -20.4567,
                                                     "y": 70.4657,
                                                     "datum": None,
                                                     "type": "GEOGRAPHIC",
                                                     "latitude": 70.4657,
                                                     "longitude": -20.4567,
                                                     "units": "DD"
                                                 }
                                             ],
                                             "vertical_extent": [
                                                 {
                                                     "value": 1500.0,
                                                     "resolution": None,
                                                     "distance_units": "feet",
                                                     "datum": "NAVD88",
                                                     "type": "ALTITUDE"
                                                 }
                                             ]
                                         },
                                         "representative": {
                                             "representative_point": None,
                                             "representative_point_type": None,
                                             "vertical_position": {
                                                 "value": -0.5,
                                                 "resolution": None,
                                                 "distance_units": "meters",
                                                 "datum": "LS",
                                                 "type": "DEPTH"
                                             }
                                         }
                                     },
                                     "description_reference": None,
                                     "related_party": [],
                                     "utc_offset": None,
                                     "url": "http://testserver/monitoringfeature/points/A-1/"
                                 }
                             ]
                         }
                         )

    def test_get_detail(self):
        response = self.client.get('/monitoringfeature/regions/A-Region1/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content.decode('utf-8')),
                         {
                             "query": {
                                 "id": "A-Region1",
                                 "feature_type": "REGION"
                             },
                             "data": {
                                 "id": "A-Region1",
                                 "name": "AwesomeRegion",
                                 "description": "This region is really awesome.",
                                 "feature_type": "REGION",
                                 "observed_properties": [],
                                 "related_sampling_feature_complex": [],
                                 "shape": "SURFACE",
                                 "coordinates": {
                                     "absolute": None,
                                     "representative": {
                                         "representative_point": {
                                             "horizontal_position": [
                                                 {
                                                     "x": -20.4567,
                                                     "y": 70.4657,
                                                     "datum": None,
                                                     "type": "GEOGRAPHIC",
                                                     "latitude": 70.4657,
                                                     "longitude": -20.4567,
                                                     "units": "DD"
                                                 }
                                             ],
                                             "vertical_extent": [
                                                 {
                                                     "value": 1500.0,
                                                     "resolution": None,
                                                     "distance_units": "feet",
                                                     "datum": "NAVD88",
                                                     "type": "ALTITUDE"
                                                 }
                                             ]
                                         },
                                         "representative_point_type": "CENTER LOCAL SURFACE",
                                         "vertical_position": None
                                     }
                                 },
                                 "description_reference": None,
                                 "related_party": [],
                                 "utc_offset": None,
                                 "url": "http://testserver/monitoringfeature/regions/A-Region1/"
                             },
                             "messages": []
                         }
                         )

    def test_get_detail_missing(self):
        response = self.client.get('/monitoringfeature/regions/A-FOO/', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json.loads(response.content.decode('utf-8')),
                         {'detail': 'There is no detail for A-FOO', 'success': False})

    def test_get_bad_id_prefix(self):
        response = self.client.get('/monitoringfeature/regions/B-FOO/', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json.loads(response.content.decode('utf-8')),
                         {'detail': 'There is no detail for B-FOO', 'success': False})


class TestMeasurementTimeseriesTVPObservationAPI(TestCase):
    """
    Test /measurement_tvp_timeseries api
    """

    VALID_OUTPUT_DATA = [
        {
            "aggregation_duration": "DAY",
            "sampling_medium": "WATER",
            "statistic": "MEAN",
            "result": {
                "value": [
                    ["2016-02-01T00:00:00", 0.3454],
                    ["2016-02-02T00:00:00", 0.6908],
                    ["2016-02-03T00:00:00", 1.0362],
                    ["2016-02-04T00:00:00", 1.3816],
                    ["2016-02-05T00:00:00", 1.7269999999999999],
                    ["2016-02-06T00:00:00", 2.0724],
                    ["2016-02-07T00:00:00", 2.4177999999999997],
                    ["2016-02-08T00:00:00", 2.7632],
                    ["2016-02-09T00:00:00", 3.1086]
                ],
                "result_quality": [
                    "VALIDATED",
                    "VALIDATED",
                    "VALIDATED",
                    "VALIDATED",
                    "VALIDATED",
                    "VALIDATED",
                    "VALIDATED",
                    "VALIDATED",
                    "VALIDATED"
                ]
            },
            "unit_of_measurement": "nm",
            "datasource": "http://testserver/datasource/A/",
            "id": "A-1",
            "type": "MEASUREMENT_TVP_TIMESERIES",
            "utc_offset": -9,
            "phenomenon_time": None,
            "observed_property": "ACT",
            "result_quality": [
                "VALIDATED"
            ],
            "feature_of_interest": {
                "id": "A-1",
                "name": "Point Location 1",
                "description": "The point.",
                "feature_type": "POINT",
                "observed_properties": [
                    "ACT",
                    "Ag",
                    "Al",
                    "Al"
                ],
                "related_sampling_feature_complex": [
                    {
                        "related_sampling_feature": "A-Region1",
                        "related_sampling_feature_type": "REGION",
                        "role": "PARENT",
                        "url": "http://testserver/monitoringfeature/regions/A-Region1/"
                    }
                ],
                "shape": "POINT",
                "coordinates": {
                    "absolute": {
                        "horizontal_position": [
                            {
                                "x": -20.4567,
                                "y": 70.4657,
                                "datum": None,
                                "type": "GEOGRAPHIC",
                                "latitude": 70.4657,
                                "longitude": -20.4567,
                                "units": "DD"
                            }
                        ],
                        "vertical_extent": [
                            {
                                "value": 1500.0,
                                "resolution": None,
                                "distance_units": "feet",
                                "datum": "NAVD88",
                                "type": "ALTITUDE"
                            }
                        ]
                    },
                    "representative": {
                        "representative_point": None,
                        "representative_point_type": None,
                        "vertical_position": {
                            "value": -0.6,
                            "resolution": None,
                            "distance_units": "meters",
                            "datum": "LS",
                            "type": "DEPTH"
                        }
                    }
                },
                "description_reference": None,
                "related_party": [],
                "utc_offset": None,
                "url": "http://testserver/monitoringfeature/points/A-1/"
            },
            "feature_of_interest_type": "POINT"
        }]
    VALID_OUTPUT = {"query": {'monitoring_feature': ['A-1'],
                              'observed_property': ['ACT'],
                              'start_date': '2016-02-01',
                              'aggregation_duration': 'DAY'},
                    'data': VALID_OUTPUT_DATA}

    ERROR_OUTPUT = {'detail': 'Missing or invalid search criteria',
                    'errors': [{'loc': ['startDate'],
                                'msg': 'invalid date format',
                                'type': 'value_error.date'}],
                    'success': False}

    def setUp(self):
        self.client = APIClient()

    def test_get(self):
        for query_string, expected_status, expected_output in [
                ("monitoring_feature=A-1&observed_property=ACT&start_date=2016-02-01", 200, self.VALID_OUTPUT),
                ("monitoring_feature=A-1&observed_property=ACT&start_date=2/1/2016", 400, self.ERROR_OUTPUT),
                ("monitoringFeature=A-1&observedProperty=ACT&startDate=2016-02-01", 200, self.VALID_OUTPUT),
                ("monitoringFeature=A-1&observedProperty=ACT&startDate=2/1/2016", 400, self.ERROR_OUTPUT)]:

            print(f"{query_string}")
            response = self.client.get(f'/measurement_tvp_timeseries/?{query_string}', format='json')
            self.assertEqual(response.status_code, expected_status)

            print(response.content.decode('utf-8'))
            assert json.loads(response.content.decode('utf-8')) == expected_output
