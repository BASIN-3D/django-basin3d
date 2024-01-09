import pytest

from basin3d.core.models import ObservedProperty
from django_basin3d.catalog import CatalogException


# # ---------------------------------------
# # Fixtures


@pytest.fixture
def catalog(monkeypatch):
    from django_basin3d.catalog import CatalogDjango
    return CatalogDjango()

# ---------------------------------------
# Tests


@pytest.mark.django_db
def test_get_observed_property(catalog):
    """Test that all of the observed property variable are returned"""
    basin3d_observed_property = catalog.find_observed_property('RDC')
    assert basin3d_observed_property == ObservedProperty(
        basin3d_vocab='RDC',
        full_name='River Discharge',
        categories=['Hydrogeology', 'Water Physical/Quality Parameters'],
        units='m2/s'
    )

    basin3d_observed_property = catalog.find_observed_property('FOO')
    assert basin3d_observed_property is None


@pytest.mark.django_db
def test_get_observed_properties(catalog):
    """Test that all of the observed property variable are returned"""

    all_basin3d_observed_properties_expected = [
        'ACT', 'ALB', 'APA', 'APR', 'AT', 'Ag', 'Al', 'As', 'B', 'BB_IN', 'BB_REF', 'Ba', 'Be', 'Br', 'CEC', 'CH4', 'CH4_d13C_soilgas',
        'CO2', 'CO2_d13C_soilgas', 'CO2_d18O_soilgas', 'Ca', 'Cd', 'Cl', 'Co', 'Cr', 'Cs', 'Cu', 'DIC', 'DIN', 'DO', 'DOC', 'DP',
        'DTN', 'EC', 'ERT', 'ET', 'EXAFS', 'Eu', 'F', 'FDOM', 'Fe2', 'FeT', 'GCC', 'GENE_TRAN', 'GWF', 'GWL', 'Ge', 'H2', 'H2O_d18O',
        'H2O_dD', 'H2S', 'HCND', 'HCND_Sat', 'HCND_Unsat', 'HCO3', 'HI', 'Hg', 'K', 'LAI', 'LSE', 'LWIR_IN', 'LWIR_REF', 'Li', 'MGO1',
        'MGO2', 'MGO3', 'MICRO_COV', 'MICRO_PEP', 'MICRO_PLFA', 'Mg', 'Mn', 'Mn2', 'Mo', 'N2', 'N2O', 'N2O_d15N_soilgas', 'N2O_d18O_soilgas',
        'NDVI', 'NH3', 'NH4', 'NIR_IN', 'NIR_REF', 'NO2', 'NO3', 'NPOC', 'Na', 'Ni', 'O2', 'ORP', 'P', 'PAI', 'PAR_IN', 'PAR_REF',
        'PFT', 'PH', 'PLT_HT', 'PO4', 'POC', 'PPT', 'PPT_SF', 'PPT_TOT_10', 'PPT_TOT_5', 'PPT_TOT_60', 'PPT_TOT_DAY', 'Pb', 'Porosity',
        'RDC', 'RET_CUR', 'RGB', 'RH', 'Rb', 'S2', 'S2O3', 'SAL', 'SAT', 'SBD', 'SC', 'SD', 'SDE', 'SDEN', 'SEC', 'SED_SIZE',
        'SEQ', 'SMO', 'SO4', 'SO4_d34S', 'SRAD', 'ST', 'STM', 'STO_RES', 'SWE', 'SWL', 'SWP', 'SYD', 'Sb', 'Se', 'Si', 'Sn', 'Sr',
        'TDS', 'TIC', 'TOC', 'TRB', 'TSS', 'Th', 'Ti', 'U', 'U235', 'UV_IN', 'UV_REF', 'V', 'WBT', 'WLE', 'WLH', 'WT', 'W_CH',
        'W_DIR', 'W_GS', 'W_SPD', 'Well logs', 'XANES', 'XRD', 'XRF', 'Zn', 'Zr', 'd13C', 'd15N']

    basin3d_observed_properties = [i.basin3d_vocab for i in catalog.find_observed_properties()]
    assert basin3d_observed_properties == all_basin3d_observed_properties_expected

    basin3d_observed_properties = [i.basin3d_vocab for i in catalog.find_observed_properties([])]
    assert basin3d_observed_properties == all_basin3d_observed_properties_expected

    basin3d_observed_properties = [i.basin3d_vocab for i in catalog.find_observed_properties(['ACT', 'ALB', 'APA', 'FOO'])]
    assert basin3d_observed_properties == ['ACT', 'ALB', 'APA']


all_datasource_vocab_mappings = [
    'DAY', 'NONE', 'Acetate', 'Ag_gas', 'Ag', 'Al', 'Aluminum', 'As', 'precip', 'daily precip', 'REJECTED',
    'UNVALIDATED', 'VALIDATED', 'max', 'mean', 'min', 'DAY', 'NONE', '01075', '01106', '01000', '01020',
    '01005', '01010', '00915', '01025', '00940', '01030', '01040', '00631', '00300', '00681', '00602',
    '01046', '50287', '00935', '00925', '01056', '01060', '00608', '00613', '00618', '00930', '01065',
    '00666', '00400', '00680', '01049', '00060', '00746', '00095', '00945', '01095', '01145', '01140',
    '70301', '01057', '80020', '63161', '00010', '01090', 'E', 'e', 'P', 'A', '00001', '00003', '00002',
    '00006']


@pytest.mark.django_db
def test_find_attribute_mappings_all(catalog):
    """Test find_observed_properties"""

    datasource_vocab = []
    for vocab in catalog.find_attribute_mappings():
        datasource_vocab.append(vocab.datasource_vocab)
    assert datasource_vocab == all_datasource_vocab_mappings


@pytest.mark.django_db
@pytest.mark.parametrize('query, expected_count, expected_list',
                         [  # all-attribute-mappings-vocab
                             ({'attr_vocab': all_datasource_vocab_mappings}, 69, []),
                             # ds_id-attr_type-attr_vocab-from_basin3d-2--Alpha-OBSERVED_PROPERTY-PPT--compound
                             ({'datasource_id': 'Alpha', 'attr_type': 'OBSERVED_PROPERTY', 'attr_vocab': 'PPT', 'from_basin3d': True}, 1,
                              [{'attr_type': 'OBSERVED_PROPERTY:SAMPLING_MEDIUM',
                                'basin3d_vocab': 'PPT:WATER',
                                'datasource': {'id': 2,
                                               'id_prefix': 'A',
                                               'location': 'https://asource.foo/',
                                               'name': 'Alpha',
                                               'plugin_class': 'AlphaDataSourcePlugin',
                                               'plugin_module': 'mybroker.plugins',
                                               'state': {'adding': False, 'db': 'default'}},
                                'basin3d_desc': [{'basin3d_vocab': 'PPT',
                                                  'full_name': 'Precipitation (Instantaneous)',
                                                  'categories': ['Climate', 'Weather'],
                                                  'units': 'mm'},
                                                 'WATER'],
                                'datasource_desc': 'precipitation',
                                'datasource_vocab': 'precip'}]),
                             # ds_id-attr_type-attr_vocab-from_basin3d--USGS-OBSERVED_PROPERTY-Hg--compound
                             ({'datasource_id': 'USGS', 'attr_type': 'OBSERVED_PROPERTY', 'attr_vocab': 'Hg', 'from_basin3d': True}, 1,
                              [{'attr_type': 'OBSERVED_PROPERTY:SAMPLING_MEDIUM',
                                'basin3d_vocab': 'Hg:WATER',
                                'datasource': {'id': 1,
                                               'id_prefix': 'USGS',
                                               'location': 'https://waterservices.usgs.gov/nwis/',
                                               'name': 'USGS',
                                               'plugin_class': 'USGSDataSourcePlugin',
                                               'plugin_module': 'basin3d.plugins.usgs',
                                               'state': {'adding': False, 'db': 'default'}},
                                'basin3d_desc': [{'basin3d_vocab': 'Hg',
                                                  'full_name': 'Mercury (Hg)',
                                                  'categories': ['Biogeochemistry', 'Trace elements'],
                                                  'units': 'mg/L'},
                                                 'WATER'],
                                'datasource_desc': 'Mercury, water, filtered, nanograms per liter',
                                'datasource_vocab': '50287'}]),
                             # ds_id-attr_type_attr_vocab-from_basin3d-similar-vocab--USGS-RESULT_QUALITY
                             ({'datasource_id': 'USGS', 'attr_type': 'RESULT_QUALITY', 'attr_vocab': ['ESTIMATED', 'VALIDATED'], 'from_basin3d': True}, 3, []),
                             # datasource_id-only-Alpha-all
                             ({'datasource_id': 'Alpha'}, 16, [],),
                             # no-params
                             ({}, 69, []),
                             # ds_id-attr_type-Alpha-STATISTIC
                             ({'datasource_id': 'Alpha', 'attr_type': 'STATISTIC'}, 3, []),
                             # ds_id-attr_type-attr_vocab--Alpha-STATISTIC-mean
                             ({'datasource_id': 'Alpha', 'attr_type': 'STATISTIC', 'attr_vocab': 'mean'}, 1, []),
                             # ds_id-attr_type_attr_vocab-from_basin3d--Alpha-STATISTIC-MEAN
                             ({'datasource_id': 'Alpha', 'attr_type': 'STATISTIC', 'attr_vocab': 'MEAN', 'from_basin3d': True}, 1, []),
                             # ds_id-attr_vocab--Alpha-mean
                             ({'datasource_id': 'Alpha', 'attr_vocab': 'mean'}, 1,
                              [{'attr_type': 'STATISTIC',
                                'basin3d_vocab': 'MEAN',
                                'datasource': {'id': 2,
                                               'id_prefix': 'A',
                                               'location': 'https://asource.foo/',
                                               'name': 'Alpha',
                                               'plugin_class': 'AlphaDataSourcePlugin',
                                               'plugin_module': 'mybroker.plugins',
                                               'state': {'adding': False, 'db': 'default'}},
                                'basin3d_desc': ['MEAN'],
                                'datasource_desc': '',
                                'datasource_vocab': 'mean'}]),
                             # ds_id-attr_vocab-from_basin3d--Alpha-MEAN
                             ({'datasource_id': 'Alpha', 'attr_vocab': 'MEAN', 'from_basin3d': True}, 1,
                              [{'attr_type': 'STATISTIC',
                                'basin3d_vocab': 'MEAN',
                                'datasource': {'id': 2,
                                               'id_prefix': 'A',
                                               'location': 'https://asource.foo/',
                                               'name': 'Alpha',
                                               'plugin_class': 'AlphaDataSourcePlugin',
                                               'plugin_module': 'mybroker.plugins',
                                               'state': {'adding': False, 'db': 'default'}},
                                'basin3d_desc': ['MEAN'],
                                'datasource_desc': '',
                                'datasource_vocab': 'mean'}]),
                             # attr_type_attr_vocab--STATISTIC-mean
                             ({'attr_type': 'STATISTIC', 'attr_vocab': 'mean'}, 1,
                              [{'attr_type': 'STATISTIC',
                                'basin3d_vocab': 'MEAN',
                                'datasource': {'id': 2,
                                               'id_prefix': 'A',
                                               'location': 'https://asource.foo/',
                                               'name': 'Alpha',
                                               'plugin_class': 'AlphaDataSourcePlugin',
                                               'plugin_module': 'mybroker.plugins',
                                               'state': {'adding': False, 'db': 'default'}},
                                'basin3d_desc': ['MEAN'],
                                'datasource_desc': '',
                                'datasource_vocab': 'mean'}]),
                             # attr_type_attr_vocab-from_basin3d--STATISTIC-MEAN
                             ({'attr_type': 'STATISTIC', 'attr_vocab': 'MEAN', 'from_basin3d': True}, 2,
                              [{'attr_type': 'STATISTIC',
                                'basin3d_vocab': 'MEAN',
                                'datasource': {'id': 2,
                                               'id_prefix': 'A',
                                               'location': 'https://asource.foo/',
                                               'name': 'Alpha',
                                               'plugin_class': 'AlphaDataSourcePlugin',
                                               'plugin_module': 'mybroker.plugins',
                                               'state': {'adding': False, 'db': 'default'}},
                                'basin3d_desc': ['MEAN'],
                                'datasource_desc': '',
                                'datasource_vocab': 'mean'},
                               {'attr_type': 'STATISTIC',
                                'basin3d_vocab': 'MEAN',
                                'datasource': {'id': 1,
                                               'id_prefix': 'USGS',
                                               'location': 'https://waterservices.usgs.gov/nwis/',
                                               'name': 'USGS',
                                               'plugin_class': 'USGSDataSourcePlugin',
                                               'plugin_module': 'basin3d.plugins.usgs',
                                               'state': {'adding': False, 'db': 'default'}},
                                'basin3d_desc': ['MEAN'],
                                'datasource_desc': '',
                                'datasource_vocab': '00003'}
                               ]),
                             # attr_type--AGGREGATION_TYPE
                             ({'attr_type': 'AGGREGATION_DURATION'}, 4, []),
                             # attr_vocab--Aluminum
                             ({'attr_vocab': 'Aluminum'}, 1, []),
                             # attr_vocab-from_basin3d--Al
                             ({'attr_vocab': 'Al', 'from_basin3d': True}, 3, []),
                             # attr_vocabs--Aluminum,Acetate
                             ({'attr_vocab': ['Aluminum', 'Acetate']}, 2, []),
                             # attr_vocabs-from_basin3d--ACT,Al
                             ({'attr_vocab': ['Al', 'ACT'], 'from_basin3d': True}, 4, []),
                             # attr_vocabs-some_bad--Aluminum,Acetate,Foo
                             ({'attr_vocab': ['Aluminum', 'Acetate', 'Foo']}, 2, []),
                             # BAD-ds_id
                             ({'datasource_id': 'Foo'}, 0, []),
                             # BAD-attr_type
                             ({'attr_type': 'BAD_ATTR_TYPE'}, 0, []),
                             # BAD-attr_vocab_type
                             ({'attr_vocab': {'foo': 'foo'}}, -1, []),
                             # No-results
                             ({'datasource_id': 'Alpha', 'attr_type': 'OBSERVED_PROPERTY', 'attr_vocab': 'Hg'}, 0, []),
                             # No-results-from_basin3d
                             ({'datasource_id': 'Alpha', 'attr_type': 'OBSERVED_PROPERTY', 'attr_vocab': 'Hg', 'from_basin3d': True}, 0, [])
                         ],
                         ids=['all-attribute-mappings-vocab', 'Alpha-from_basin3d', 'USGS-from_basin3d', 'ds_id-attr_type_attr_vocab-from_basin3d-similar-vocab',
                              'datasource_id-only-Alpha-all', 'no-params', 'ds_id-attr_type-Alpha-STATISTIC', 'ds_id-attr_type-attr_vocab--Alpha-STATISTIC-mean',
                              'ds_id-attr_type_attr_vocab-from_basin3d--Alpha-STATISTIC-MEAN', 'ds_id-attr_vocab--Alpha-mean', 'ds_id-attr_vocab-from_basin3d--Alpha-MEAN',
                              'attr_type_attr_vocab--STATISTIC-mean', 'attr_type_attr_vocab-from_basin3d--STATISTIC-MEAN', 'attr_type--AGGREGATION_TYPE',
                              'attr_vocab--Aluminum', 'attr_vocab-from_basin3d--Al', 'attr_vocabs--Aluminum,Acetate', 'attr_vocabs-from_basin3d--ACT,Al',
                              'attr_vocabs-some_bad--Aluminum,Acetate,Foo', 'BAD-ds_id', 'BAD-attr_type', 'BAD-attr_vocab_type', 'No-results',
                              'No-results-from_basin3d']
                         )
def test_find_attribute_mappings(catalog, query, expected_count, expected_list):
    attribute_mappings = catalog.find_attribute_mappings(**query)

    actual_list = []
    if expected_count >= 0:
        count = 0
        for attr_mapping in attribute_mappings:
            if attr_mapping is None:
                continue
            count += 1
            if expected_list:
                actual_list.append(attr_mapping.to_dict())
        assert count == expected_count
        if expected_list:
            for expected_attr_mapping in expected_list:
                assert expected_attr_mapping in actual_list
    else:
        with pytest.raises(CatalogException):
            for attr_mapping in attribute_mappings:
                pass


@pytest.mark.django_db
@pytest.mark.parametrize("query, expected",
                         [({'datasource_vocab': 'FOO', "datasource_id": 'Alpha', 'attr_type': 'OBSERVED_PROPERTY'},
                          {'attr_type': 'OBSERVED_PROPERTY',
                           'basin3d_desc': [],
                           'basin3d_vocab': 'NOT_SUPPORTED',
                           'datasource': {'id': 2,
                                          'id_prefix': 'A',
                                          'location': 'https://asource.foo/',
                                          'name': 'Alpha',
                                          'plugin_class': 'AlphaDataSourcePlugin',
                                          'plugin_module': 'mybroker.plugins',
                                          'state': {'adding': False, 'db': 'default'}},
                           'datasource_desc': 'No mapping was found for attr: "OBSERVED_PROPERTY" and '
                                              'for datasource vocab: "FOO" in datasource: "Alpha".',
                           'datasource_vocab': 'FOO'},
                           ),
                          ({"datasource_id": 'USGS', 'datasource_vocab': '50287', 'attr_type': 'OBSERVED_PROPERTY'},
                           {'attr_type': 'OBSERVED_PROPERTY:SAMPLING_MEDIUM',
                            'basin3d_vocab': 'Hg:WATER',
                            'datasource': {'id': 1,
                                           'id_prefix': 'USGS',
                                           'location': 'https://waterservices.usgs.gov/nwis/',
                                           'name': 'USGS',
                                           'plugin_class': 'USGSDataSourcePlugin',
                                           'plugin_module': 'basin3d.plugins.usgs',
                                           'state': {'adding': False, 'db': 'default'}},
                            'basin3d_desc': [{'basin3d_vocab': 'Hg',
                                              'full_name': 'Mercury (Hg)',
                                              'categories': ['Biogeochemistry', 'Trace elements'],
                                              'units': 'mg/L'},
                                             'WATER'],
                            'datasource_desc': 'Mercury, water, filtered, nanograms per liter',
                            'datasource_vocab': '50287'}
                           ),
                          ({"datasource_id": 'Alpha', 'datasource_vocab': 'Acetate', 'attr_type': 'OBSERVED_PROPERTY'},
                           {'attr_type': 'OBSERVED_PROPERTY:SAMPLING_MEDIUM',
                            'basin3d_vocab': 'ACT:WATER',
                            'datasource': {'id': 2,
                                           'id_prefix': 'A',
                                           'location': 'https://asource.foo/',
                                           'name': 'Alpha',
                                           'plugin_class': 'AlphaDataSourcePlugin',
                                           'plugin_module': 'mybroker.plugins',
                                           'state': {'adding': False, 'db': 'default'}},
                            'basin3d_desc': [{'basin3d_vocab': 'ACT',
                                              'full_name': 'Acetate (CH3COO)',
                                              'categories': ['Biogeochemistry', 'Anions'],
                                              'units': 'mM'},
                                             'WATER'],
                            'datasource_desc': 'acetate',
                            'datasource_vocab': 'Acetate'},
                           ),
                          ({"datasource_id": 'FOO', 'datasource_vocab': 'Acetate', 'attr_type': 'OBSERVED_PROPERTY'},
                           {'attr_type': 'OBSERVED_PROPERTY',
                            'basin3d_desc': [],
                            'basin3d_vocab': 'NOT_SUPPORTED',
                            'datasource': {'id': None,
                                           'id_prefix': None,
                                           'location': None,
                                           'name': None,
                                           'plugin_class': None,
                                           'plugin_module': None,
                                           'state': {}},
                            'datasource_desc': 'No Data Source "FOO" found.',
                            'datasource_vocab': 'Acetate'}
                           )
                          ],
                         ids=['Wrong-Alpha', 'USGS-plus', 'Alpha-plus', 'Bad-DataSource'])
def test_find_datasource_attribute_mapping(catalog, query, expected):
    """ Test observed property """

    attr_mapping = catalog.find_datasource_attribute_mapping(**query)
    assert attr_mapping.to_dict() == expected
