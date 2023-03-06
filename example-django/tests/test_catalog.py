import logging
import pytest

log = logging.Logger(__name__)

# # ---------------------------------------
# # Fixtures


@pytest.fixture
def catalog(monkeypatch):
    from django_basin3d.catalog import CatalogDjango
    return CatalogDjango()

# ---------------------------------------
# Tests


@pytest.mark.django_db
def test_get_observed_property_variables(catalog):
    """Test that all of the observed property variable are returned"""
    basin3d_variable = [i.basin3d_id for i in catalog.find_observed_property_variables()]

    assert basin3d_variable == ['PH', 'RDC', 'WLE', 'WT', 'DO', 'SC', 'TDS', 'DIN', 'DTN', 'NH4', 'POC', 'DOC', 'P',
                                'Na', 'K', 'Mg', 'Ca', 'Si', 'Cl', 'SO4', 'NO3', 'NO2', 'S2', 'B', 'Al', 'Sb', 'As',
                                'Ba', 'Be', 'Cd', 'Cr', 'Cu', 'FeT', 'Pb', 'Mo', 'Mn', 'Hg', 'Ni', 'Se', 'Ag', 'Th',
                                'U', 'Zn', 'ACT', 'Ag', 'Al', 'As']


@pytest.mark.django_db
def test_find_observed_properties(catalog):
    """Test find_observed_properties"""

    expected = ['00400', '00060', '63161', '00010', '00300', '00095', '70301', '00631', '00602', '00608', '00680',
                '00681', '00666', '00930', '00935', '00925', '00915', '01140', '00940', '00945', '00618', '00613',
                '00746', '01020', '01106', '01095', '01000', '01005', '01010', '01025', '01030', '01040', '01046',
                '01049', '01060', '01056', '50287', '01065', '01145', '01075', '01057', '80020', '01090', 'Acetate',
                'Ag', 'Aluminium', 'As']

    datasource_variables = []
    for idx, item in enumerate(catalog.find_observed_properties()):
        datasource_variables.append(item.datasource_variable)
    assert datasource_variables == expected


@pytest.mark.django_db
@pytest.mark.parametrize("query, expected",
                         [({'variable_name': 'FOO', "datasource_id": 'Alpha'}, None),
                          ({"datasource_id": 'USGS', 'variable_name': 'Hg'}, {'datasource': {'credentials': {},
                                                                                             'id': 'USGS',
                                                                                             'id_prefix': 'USGS',
                                                                                             'location': 'https://waterservices.usgs.gov/nwis/',
                                                                                             'name': 'USGS'},
                                                                              'datasource_description': 'USGS',
                                                                              'datasource_variable': '50287',
                                                                              'observed_property_variable': {
                                                                                  'basin3d_id': 'Hg',
                                                                                  'categories': ['Biogeochemistry',
                                                                                                 'Trace elements'],
                                                                                  'full_name': 'Mercury (Hg)',
                                                                                  'units': ''},
                                                                              'sampling_medium': 'WATER'}),
                          ({"datasource_id": 'Alpha', 'variable_name': 'ACT'}, {'datasource': {'credentials': {},
                                                                                               'id': 'Alpha',
                                                                                               'id_prefix': 'A',
                                                                                               'location': 'https://asource.foo/',
                                                                                               'name': 'Alpha'},
                                                                                'datasource_description': 'Alpha',
                                                                                'datasource_variable': 'Acetate',
                                                                                'observed_property_variable': {
                                                                                    'basin3d_id': 'ACT',
                                                                                    'categories': ['Biogeochemistry',
                                                                                                   'Anions'],
                                                                                    'full_name': 'Acetate (CH3COO)',
                                                                                    'units': ''},
                                                                                'sampling_medium': 'WATER'}),
                          ({"datasource_id": 'FOO', 'variable_name': 'ACT'}, None)
                          ],
                         ids=['Wrong-Alpha', 'USGS-plus', 'Alpha-plus', 'Bad-DataSource'])
def test_observed_property(catalog, query, expected):
    """ Test observed property """

    observed_property = catalog.find_observed_property(**query)
    if expected is None:
        assert observed_property == expected
    else:
        assert observed_property.to_dict() == expected
