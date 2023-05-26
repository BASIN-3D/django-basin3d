import pytest

from django.db.models import ObjectDoesNotExist
from django.test import TestCase

from django_basin3d.models import DataSource, ObservedProperty, AttributeMapping


class DataSourceTestCase(TestCase):
    def setUp(self):
        DataSource.objects.create(name="Foo", plugin_module="foo.bar.plugins", plugin_class="Baz", id_prefix="F")
        DataSource.objects.create(name="Bar", plugin_module="foo.plugins", plugin_class="Bar", id_prefix="B")

    def test_get(self):
        """Assert that the Data Sources were created"""
        foo = DataSource.objects.get(name="Foo")
        bar = DataSource.objects.get(name="Bar")
        self.assertEqual(bar.name, "Bar")
        self.assertEqual(foo.name, 'Foo')


class AttributeMappingTestCase(TestCase):
    """
    Assert that the parameters are created
    """
    def setUp(self):
        """
        Load some fake data to use in the tests
        """
        self.datasource = DataSource.objects.get(name="Alpha")
        self.desc = [{
            'basin3d_vocab': 'FOO',
            'full_name': 'Acetate (CH3COO)',
            'categories': ['Biogeochemistry', 'Anions'],
            'units': 'mM'},
            'WATER']

    def test_attribute_mapping_create(self):
        """ Was the object created correctly? """

        obj = AttributeMapping(attr_type='OBSERVED_PROPERTY:SAMPLING_MEDIUM',
                               basin3d_vocab='ACT:WATER',
                               basin3d_desc=self.desc,
                               datasource_vocab='FOO',
                               datasource_desc='FOO desc',
                               datasource=self.datasource)

        assert obj.attr_type == 'OBSERVED_PROPERTY:SAMPLING_MEDIUM'
        assert obj.basin3d_vocab == 'ACT:WATER'
        assert obj.basin3d_desc == self.desc
        assert obj.datasource_vocab == 'FOO'
        assert obj.datasource_desc == 'FOO desc'
        assert obj.datasource == self.datasource


class ObservedPropertyTestCase(TestCase):
    """
    Test the Observed Property Model
    """

    def setUp(self):
        ObservedProperty.objects.create(basin3d_vocab='ZZZ', full_name='Zzz', categories='Z,z', units='z')

    def test_observed_property_create(self):

        obj = ObservedProperty(
            basin3d_vocab='FOO',
            full_name='Foo',
            categories='FOO,Foo',
            units='ff')

        assert obj.basin3d_vocab == 'FOO'
        assert obj.full_name == 'Foo'
        assert obj.categories == 'FOO,Foo'
        assert obj.units == 'ff'

    def test_get(self):
        op1 = ObservedProperty.objects.get(pk='ZZZ')

        assert op1.basin3d_vocab == 'ZZZ'
        assert op1.full_name == 'Zzz'
        assert op1.categories == 'Z,z'
        assert op1.units == 'z'

        with pytest.raises(ObjectDoesNotExist):
            ObservedProperty.objects.get(pk='YYY')
