from basin3d.core.schema.enum import FeatureTypeEnum, ResultQualityEnum, MappedAttributeEnum
from basin3d.core.types import SpatialSamplingShapes

from django_basin3d.models import DataSource
from basin3d.core.models import MonitoringFeature, Coordinate, \
    AbsoluteCoordinate, RepresentativeCoordinate, GeographicCoordinate, AltitudeCoordinate, \
    DepthCoordinate, VerticalCoordinate, RelatedSamplingFeature, Observation, \
    MeasurementTimeseriesTVPObservation, TimeValuePair, ResultListTVP, MappedAttribute, AttributeMapping
from django.test import TestCase


class ModelTests(TestCase):
    def setUp(self):
        self.datasource = DataSource.objects.get(name="Alpha")
        self.plugin_access = self.datasource.get_plugin().get_plugin_access()[MeasurementTimeseriesTVPObservation]

    def test_representative_coordinate(self):
        """Test a Representative Coordinatge"""

        r_coord = RepresentativeCoordinate(
            representative_point=AbsoluteCoordinate(
                horizontal_position=GeographicCoordinate(
                    units=GeographicCoordinate.UNITS_DEC_DEGREES,
                    latitude=70.4657, longitude=-20.4567),
                vertical_extent=AltitudeCoordinate(
                    datum=AltitudeCoordinate.DATUM_NAVD88,
                    value=1500, distance_units=VerticalCoordinate.DISTANCE_UNITS_FEET)),
            representative_point_type=RepresentativeCoordinate.REPRESENTATIVE_POINT_TYPE_CENTER_LOCAL_SURFACE)

        assert r_coord.representative_point.vertical_extent[0].datum == AltitudeCoordinate.DATUM_NAVD88
        assert r_coord.representative_point.vertical_extent[0].value == 1500
        assert r_coord.representative_point.vertical_extent[0].distance_units == VerticalCoordinate.DISTANCE_UNITS_FEET
        assert r_coord.representative_point.horizontal_position[0].longitude == -20.4567
        assert r_coord.representative_point.horizontal_position[0].x == -20.4567
        assert r_coord.representative_point.horizontal_position[0].y == 70.4657
        assert r_coord.representative_point.horizontal_position[0].latitude == 70.4657
        assert r_coord.representative_point.horizontal_position[0].units == GeographicCoordinate.UNITS_DEC_DEGREES
        assert r_coord.representative_point_type == RepresentativeCoordinate.REPRESENTATIVE_POINT_TYPE_CENTER_LOCAL_SURFACE \


    def test_related_sampling_feature(self):
        """Test a Related Sampling feature"""
        related_sampling_feature = RelatedSamplingFeature(plugin_access=self.plugin_access,
                                                          related_sampling_feature="Region1",
                                                          related_sampling_feature_type=FeatureTypeEnum.REGION,
                                                          role=RelatedSamplingFeature.ROLE_PARENT)

        assert related_sampling_feature.datasource == self.plugin_access.datasource
        assert related_sampling_feature.related_sampling_feature == "A-Region1"
        assert related_sampling_feature.related_sampling_feature_type == FeatureTypeEnum.REGION
        assert related_sampling_feature.role == RelatedSamplingFeature.ROLE_PARENT

    def test_absolute_coordinate(self):
        a_coord = AltitudeCoordinate(
            datum=AltitudeCoordinate.DATUM_NAVD88,
            value=1500,
            distance_units=VerticalCoordinate.DISTANCE_UNITS_FEET)

        assert a_coord.datum == AltitudeCoordinate.DATUM_NAVD88
        assert a_coord.value == 1500
        assert a_coord.distance_units == VerticalCoordinate.DISTANCE_UNITS_FEET

    def test_monitoring_feature_create(self):
        """
        Test instance of monitoring feature
        :return: n/a
        """

        a_region = MonitoringFeature(
            plugin_access=self.plugin_access,
            id="Region1",
            name="AwesomeRegion",
            description="This region is really awesome.",
            feature_type=FeatureTypeEnum.REGION,
            shape=SpatialSamplingShapes.SHAPE_SURFACE,
            coordinates=Coordinate(representative=RepresentativeCoordinate(
                representative_point=AbsoluteCoordinate(
                    horizontal_position=GeographicCoordinate(
                        units=GeographicCoordinate.UNITS_DEC_DEGREES,
                        latitude=70.4657, longitude=-20.4567),
                    vertical_extent=AltitudeCoordinate(
                        datum=AltitudeCoordinate.DATUM_NAVD88,
                        value=1500, distance_units=VerticalCoordinate.DISTANCE_UNITS_FEET)),
                representative_point_type=RepresentativeCoordinate.REPRESENTATIVE_POINT_TYPE_CENTER_LOCAL_SURFACE)
            )
        )

        assert a_region.datasource.name == "Alpha"
        assert a_region.id == "A-Region1"
        assert a_region.name == "AwesomeRegion"
        assert a_region.feature_type == FeatureTypeEnum.REGION
        assert a_region.description == "This region is really awesome."
        assert a_region.shape == SpatialSamplingShapes.SHAPE_SURFACE
        assert a_region.coordinates.representative.representative_point.horizontal_position[0].units == \
            GeographicCoordinate.UNITS_DEC_DEGREES
        assert a_region.coordinates.representative.representative_point.horizontal_position[0].latitude == 70.4657
        assert a_region.coordinates.representative.representative_point.horizontal_position[0].longitude == -20.4567
        assert a_region.coordinates.representative.representative_point.vertical_extent[0].datum == \
            AltitudeCoordinate.DATUM_NAVD88
        assert a_region.coordinates.representative.representative_point.vertical_extent[0].value == 1500
        assert a_region.coordinates.representative.representative_point.vertical_extent[0].distance_units == \
            VerticalCoordinate.DISTANCE_UNITS_FEET
        assert a_region.coordinates.representative.representative_point_type == \
            RepresentativeCoordinate.REPRESENTATIVE_POINT_TYPE_CENTER_LOCAL_SURFACE

        a_point = MonitoringFeature(
            plugin_access=self.plugin_access,
            id="1",
            name="Point Location 1",
            description="The first point.",
            feature_type=FeatureTypeEnum.POINT,
            shape=SpatialSamplingShapes.SHAPE_POINT,
            coordinates=Coordinate(
                absolute=AbsoluteCoordinate(
                    horizontal_position=GeographicCoordinate(
                        units=GeographicCoordinate.UNITS_DEC_DEGREES,
                        latitude=70.4657, longitude=-20.4567),
                    vertical_extent=AltitudeCoordinate(
                        datum=AltitudeCoordinate.DATUM_NAVD88,
                        value=1500,
                        distance_units=VerticalCoordinate.DISTANCE_UNITS_FEET)),
                representative=RepresentativeCoordinate(
                    vertical_position=DepthCoordinate(
                        datum=DepthCoordinate.DATUM_LOCAL_SURFACE,
                        value=-0.5, distance_units=VerticalCoordinate.DISTANCE_UNITS_METERS)
                )
            ),
            observed_properties=["Ag", "Acetate"],
            related_sampling_feature_complex=[
                RelatedSamplingFeature(plugin_access=self.plugin_access,
                                       related_sampling_feature="Region1",
                                       related_sampling_feature_type=FeatureTypeEnum.REGION,
                                       role=RelatedSamplingFeature.ROLE_PARENT)]
        )

        assert a_point.datasource.name == "Alpha"
        assert a_point.id == "A-1"
        assert a_point.name == "Point Location 1"
        assert a_point.feature_type == FeatureTypeEnum.POINT
        assert a_point.description == "The first point."
        assert a_point.shape == SpatialSamplingShapes.SHAPE_POINT
        assert a_point.coordinates.absolute.horizontal_position[0].units == \
            GeographicCoordinate.UNITS_DEC_DEGREES
        assert a_point.coordinates.absolute.horizontal_position[0].latitude == 70.4657
        assert a_point.coordinates.absolute.horizontal_position[0].longitude == -20.4567
        assert a_point.coordinates.absolute.vertical_extent[0].datum == \
            AltitudeCoordinate.DATUM_NAVD88
        assert a_point.coordinates.absolute.vertical_extent[0].value == 1500
        assert a_point.coordinates.absolute.vertical_extent[0].distance_units == \
            VerticalCoordinate.DISTANCE_UNITS_FEET
        assert a_point.coordinates.representative.vertical_position.value == -0.5
        assert a_point.coordinates.representative.vertical_position.distance_units == \
            VerticalCoordinate.DISTANCE_UNITS_METERS
        assert a_point.coordinates.representative.vertical_position.datum == \
            DepthCoordinate.DATUM_LOCAL_SURFACE
        op_list = a_point.observed_properties
        assert [op.get_basin3d_vocab() for op in op_list] == ["Ag", "ACT"]
        assert a_point.related_sampling_feature_complex[0].related_sampling_feature == "A-Region1"
        assert a_point.related_sampling_feature_complex[0].role == "PARENT"

    def test_observation_create(self):
        """
        Test instance of observation model class
        NOTE: In practice, the Observation should not be used stand alone
        :return: n/a
        """
        obs01 = Observation(
            plugin_access=self.plugin_access,
            id="timeseries01",
            utc_offset="9",
            phenomenon_time="20180201",
            result_quality=[ResultQualityEnum.VALIDATED],
            feature_of_interest="Point011")

        assert obs01.datasource.name == "Alpha"
        assert obs01.id == "A-timeseries01"
        assert obs01.utc_offset == "9"
        assert obs01.phenomenon_time == "20180201"
        assert obs01.observed_property is None
        assert obs01.result_quality[0].to_json() == MappedAttribute(
            attr_type=MappedAttributeEnum.RESULT_QUALITY,
            attr_mapping=AttributeMapping(
                attr_type='RESULT_QUALITY',
                basin3d_vocab='VALIDATED', basin3d_desc=[ResultQualityEnum.VALIDATED],
                datasource_vocab='VALIDATED', datasource_desc='',
                datasource=self.datasource)).to_json()
        assert obs01.feature_of_interest == "Point011"

    def test_measurement_timeseries_tvp_observation_create(self):
        """
        Test instance of Measurement Timeseries TVP Observation
        :return: n/a
        """
        obs01 = MeasurementTimeseriesTVPObservation(
            plugin_access=self.plugin_access,
            id="timeseries01",
            utc_offset="9",
            phenomenon_time="20180201",
            result_quality=["VALIDATED"],
            feature_of_interest="Point011",
            feature_of_interest_type=FeatureTypeEnum.POINT,
            aggregation_duration="DAY",
            time_reference_position="start",
            observed_property="Acetate",
            statistic="mean",
            result=ResultListTVP(plugin_access=self.plugin_access,
                                 value=[TimeValuePair("201802030100", "5.32")],
                                 result_quality=['VALIDATED']),
            unit_of_measurement="m"
        )

        assert obs01.datasource.name == "Alpha"
        assert obs01.id == "A-timeseries01"
        assert obs01.utc_offset == "9"
        assert obs01.phenomenon_time == "20180201"
        assert obs01.observed_property is not None
        assert isinstance(obs01.observed_property, MappedAttribute) is True
        assert obs01.observed_property.get_basin3d_vocab() == "ACT"
        assert obs01.result_quality[0].get_basin3d_vocab() == "VALIDATED"
        assert obs01.feature_of_interest == "Point011"
        assert obs01.feature_of_interest_type == FeatureTypeEnum.POINT
        assert obs01.aggregation_duration.get_basin3d_vocab() == "DAY"
        assert obs01.time_reference_position == "start"
        assert obs01.statistic.get_basin3d_vocab() == "MEAN"
        assert obs01.unit_of_measurement == "m"
