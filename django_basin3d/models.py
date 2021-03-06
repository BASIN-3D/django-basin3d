"""
`django_basin3d.models`
****************

.. currentmodule:: django_basin3d.models

:synopsis: The BASIN-3D  Models
:module author: Val Hendrix <vhendrix@lbl.gov>
:module author: Danielle Svehla Christianson <dschristianson@lbl.gov>

Below is the inheritance diagram for BASIN-3D generic models and supporting classes.  All of the models are based on
:class:`django.db.models.Model` which provide the object relational mapping technology for building and managing
relational database tables.

.. inheritance-diagram:: django_basin3d.models
    :top-classes: django.db.models.Model, django.db.models.fields.TextField

.. contents:: Contents
    :local:
    :backlinks: top



"""
from __future__ import unicode_literals

from importlib import import_module
from typing import List

from django.db import models


class SpatialSamplingShapes(object):
    """
    Spatial sampling shape describing a spatial sampling feature

    Controlled CV list as defined by OGC Observation & Measurement GM_Shape.
    """

    #: The shape of a spatially extensive sampling feature which provides a complete sampling domain.
    SHAPE_SOLID = "SOLID"

    #: The shape of a spatially extensive sampling feature which provides a complete sampling domain.
    SHAPE_SURFACE = "SURFACE"

    #: The shape of a spatially extensive sampling feature which provides a complete sampling domain.
    SHAPE_CURVE = "CURVE"

    #: The shape of a spatially extensive sampling feature which provides a complete sampling domain.
    SHAPE_POINT = "POINT"


class FeatureTypes(object):
    """
    Feature Types where an Observation can be made.

    Controlled CV list that is maintained. USGS Watershed Boundry Dataset is used.
    The goal is to strike a balance between commonly used hierarchical levels and features
    versus a runaway list of FeatureTypes. OGC O&M suggests that Features should be
    determined as needed.
    """

    REGION = 0
    SUBREGION = 1
    BASIN = 2
    SUBBASIN = 3
    WATERSHED = 4
    SUBWATERSHED = 5
    SITE = 6
    PLOT = 7
    HORIZONTAL_PATH = 8  # Rivers, Transects
    VERTICAL_PATH = 9  # Towers, Boreholes, Trees, Pits
    POINT = 10

    TYPES = {
        REGION: "REGION",
        SUBREGION: "SUBREGION",
        BASIN: "BASIN",
        SUBBASIN: "SUBBASIN",
        WATERSHED: "WATERSHED",
        SUBWATERSHED: "SUBWATERSHED",
        SITE: "SITE",
        PLOT: "PLOT",
        HORIZONTAL_PATH: "HORIZONTAL PATH",
        VERTICAL_PATH: "VERTICAL PATH",
        POINT: "POINT"
    }

    SHAPE_TYPES = {
        SpatialSamplingShapes.SHAPE_POINT: [POINT],
        SpatialSamplingShapes.SHAPE_CURVE: [HORIZONTAL_PATH, VERTICAL_PATH],
        SpatialSamplingShapes.SHAPE_SURFACE: [REGION, SUBREGION, BASIN, SUBBASIN, WATERSHED,
                                              SUBWATERSHED, SITE, PLOT],
        SpatialSamplingShapes.SHAPE_SOLID: []
    }


def get_feature_types() -> List[str]:
    """
    Helper function for FeatureTypes
    :return list of feature_types as strings
    """
    return [x for x in FeatureTypes.TYPES.values()]


class StringListField(models.TextField):
    """
    StringListField stored delimited strings in the database.

    :param: delimiter
    :type: str
    """

    def __init__(self, *args, **kwargs):
        self.delimiter = ","
        if "delimiter" in kwargs.keys():
            self.delimiter = kwargs["delimiter"]

        super(StringListField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            value = []

        if isinstance(value, list) or isinstance(value, tuple):
            return value
        elif isinstance(value, str):
            return value.split(self.delimiter)

        raise ValueError("ListField must be  delimited string")

    def get_prep_value(self, value):
        if value is None:
            return value
        else:
            return value

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return self.get_db_prep_value(value, None)


class DataSource(models.Model):
    """
    Data Source definition

    Attributes:
        - *id:* string (inherited)
        - *name:* string
        - *id_prefix:* string, prefix that is added to all data source ids
        - *plugin_module:*
        - *plugin_class:*
        - *credentials:*
        - *enabled:*

    """
    name = models.CharField(max_length=20, unique=True, blank=False)
    id_prefix = models.CharField(max_length=5, unique=True, blank=False)
    location = models.TextField(blank=True)
    plugin_module = models.TextField(blank=True)
    plugin_class = models.TextField(blank=True)

    class Meta:
        ordering = ['id_prefix']

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return '<DataSource %r>' % (self.name)

    def get_plugin(self):
        """
        Return the plugin class
        """

        module = import_module(self.plugin_module)
        plugin_class = getattr(module, self.plugin_class)
        from django_basin3d.catalog import CatalogDjango
        return plugin_class(CatalogDjango())


class ObservedProperty(models.Model):
    """
    Defining the attributes for a single/multiple Observed Properties

    Attributes:
        - *id:* string, e.g., Cs137 MID
        - *description:* id, e.g., Cs 137 air dose rate car survey campaigns
        - *observed_property_variable_id:* string, e.g., Cs137MVID
        - *sampling_medium:* enum (WATER, GAS, SOLID PHASE, OTHER, NOT APPLICABLE)
    """

    description = models.TextField(null=True, blank=True)
    observed_property_variable = models.ForeignKey('ObservedPropertyVariable', null=False, on_delete=models.CASCADE)
    sampling_medium = models.ForeignKey('SamplingMedium', null=False, on_delete=models.DO_NOTHING)
    datasource = models.ForeignKey('DataSource', null=False, on_delete=models.DO_NOTHING)

    class Meta:
        unique_together = ('observed_property_variable', 'datasource')

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return self.description

    def __repr__(self):
        return '<ObservedProperty %r>' % (self.description)


class ObservedPropertyVariable(models.Model):
    """
    Defining the properties being observed (measured). See http://vocabulary.odm2.org/variablename/ for controlled vocabulary

    Attributes:
        - *id:* string,
        - *full_name:* string,
        - *abbreviation:* string,
        - *categories:* Array of strings (in order of priority).

    See http://vocabulary.odm2.org/variabletype/ for options, although I think we should have our own list (theirs is a bit funky).


    """

    # Unique string Identifier for the Observed Property Variable
    basin3d_id = models.CharField(max_length=50, unique=True, blank=False, primary_key=True)

    # Long name of the Observed Property Variable
    full_name = models.CharField(max_length=255)

    # Ordered list of categories
    categories = StringListField(blank=True, null=True)

    class Meta:
        ordering = ('basin3d_id',)

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return self.full_name

    def __repr__(self):
        return "<ObservedPropertyVariable {}>".format(self.id)


class DataSourceObservedPropertyVariable(models.Model):
    """
    Synthesis of Data Source Observed Property Variables with BASIN-3D Observed Property Variables
    """
    datasource = models.ForeignKey(DataSource, on_delete=models.DO_NOTHING)
    observed_property_variable = models.ForeignKey(ObservedPropertyVariable,
                                                   on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=255, blank=False)

    class Meta:
        unique_together = (("datasource", "observed_property_variable"),)

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return '<DataSourceObservedPropertyVariable %r>' % (self.name)


class SamplingMedium(models.Model):
    """
    Types of sampling mediums for Observed Properties
    """

    SOLID_PHASE = "SOLID PHASE"
    WATER = "WATER"
    GAS = "GAS"
    OTHER = "OTHER"
    NOT_APPLICABLE = "N/A"
    SAMPLING_MEDIUMS = [WATER, GAS, SOLID_PHASE, OTHER, NOT_APPLICABLE]

    name = models.CharField(max_length=50, null=False, blank=False, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return '<SamplingMedium %r>' % (self.name)
