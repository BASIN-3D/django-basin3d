import logging
from typing import Any, List

from basin3d.core.models import AbsoluteCoordinate, AltitudeCoordinate, Coordinate, DepthCoordinate, \
    GeographicCoordinate, MeasurementTimeseriesTVPObservation, MonitoringFeature, RelatedSamplingFeature, \
    RepresentativeCoordinate, SpatialSamplingShapes, VerticalCoordinate, ResultListTVP
from basin3d.core.plugin import DataSourcePluginPoint, basin3d_plugin, DataSourcePluginAccess
from basin3d.core.schema.enum import FeatureTypeEnum, TimeFrequencyEnum
from basin3d.core.schema.query import QueryMonitoringFeature, QueryMeasurementTimeseriesTVP

logger = logging.getLogger(__name__)


class AlphaMeasurementTimeseriesTVPObservationAccess(DataSourcePluginAccess):
    """
    MeasurementTimeseriesTVPObservation Access class
    """
    synthesis_model_class = MeasurementTimeseriesTVPObservation

    def list(self, query: QueryMeasurementTimeseriesTVP):
        """
        Generate a list of MeasurementTimeseriesTVPObservation objects
        """
        synthesis_messages: List[str] = []
        data: List[Any] = []
        quality: List[Any] = []

        # query = kwargs.get('query')
        # assert query

        if query.monitoring_feature == ['region']:
            return StopIteration({"message": "FOO"})

        supported_monitoring_features = [f'{num}' for num in range(1, 5)]

        if not any([loc_id in supported_monitoring_features for loc_id in query.monitoring_feature]):
            return StopIteration({"message": "No data from data source matches monitoring features specified."})

        location_indices = []
        for loc_id in query.monitoring_feature:
            if loc_id in supported_monitoring_features:
                location_indices.append(int(loc_id.split('-')[-1]))

        from datetime import datetime
        for num in range(1, 10):
            data.append((datetime(2016, 2, num), num * 0.3454))
        data = [data, data, [], data]
        rqe1 = 'VALIDATED'
        rqe2 = 'UNVALIDATED'
        rqe3 = 'REJECTED'
        quality = [[rqe1, rqe1, rqe1, rqe1, rqe1, rqe1, rqe1, rqe1, rqe1],
                   [rqe2, rqe2, rqe2, rqe2, rqe2, rqe2, rqe2, rqe3, rqe3],
                   [],
                   [rqe1, rqe2, rqe3, rqe1, rqe1, rqe1, rqe1, rqe1, rqe1]]
        qualities = [[rqe1],
                     [rqe2, rqe3],
                     [],
                     [rqe1, rqe2, rqe3]]
        observed_property_variables = ["Acetate", "Acetate", "Aluminum", "Al"]
        units = ['nm', 'nm', 'mg/L', 'mg/L']
        statistics = ['mean', 'max', 'mean', 'max']

        for num in location_indices:
            observed_property_variable = observed_property_variables[num - 1]
            feature_id = f'A-{str(num - 1)}'
            if query:
                if observed_property_variable not in query.observed_property:
                    continue
                if query.statistic:
                    if statistics[num - 1] not in query.statistic:
                        continue
                result_value = data[num - 1]
                result_value_quality = quality[num - 1]
                result_qualities = qualities[num - 1]
                if query.result_quality:
                    filtered_value = []
                    filtered_quality = []
                    has_filtered_data_points = 0

                    for v, q in zip(result_value, result_value_quality):
                        if q in query.result_quality:
                            filtered_value.append(v)
                            filtered_quality.append(q)
                        else:
                            has_filtered_data_points += 1

                    if has_filtered_data_points > 0:
                        synthesis_messages.append(f'{feature_id} - {observed_property_variable}: {str(has_filtered_data_points)} timestamps did not match data quality query.')

                    if len(filtered_value) == 0:
                        synthesis_messages.append(f'{feature_id} - {observed_property_variable}: No data values matched result_quality query.')
                        print(f'{feature_id} - {observed_property_variable}')
                        continue

                    result_value = filtered_value
                    result_value_quality = filtered_quality
                    if len(result_value_quality) > 0:
                        result_qualities = list(set(result_value_quality))
                    else:
                        result_qualities = []

            yield MeasurementTimeseriesTVPObservation(
                plugin_access=self,
                id=num,
                observed_property=observed_property_variable,
                utc_offset=-8 - num,
                feature_of_interest=MonitoringFeature(
                    plugin_access=self,
                    id=num,
                    name="Point Location " + str(num),
                    description="The point.",
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
                                value=-0.5 - num * 0.1,
                                distance_units=VerticalCoordinate.DISTANCE_UNITS_METERS)
                        )
                    ),
                    observed_properties=["Ag", "Acetate", "Aluminum", "Al"],
                    related_sampling_feature_complex=[
                        RelatedSamplingFeature(
                            plugin_access=self,
                            related_sampling_feature="Region1",
                            related_sampling_feature_type=FeatureTypeEnum.REGION,
                            role=RelatedSamplingFeature.ROLE_PARENT)]
                ),
                feature_of_interest_type=FeatureTypeEnum.POINT,
                unit_of_measurement=units[num - 1],
                aggregation_duration=TimeFrequencyEnum.DAY,
                result_quality=result_qualities,
                time_reference_position=None,
                statistic=statistics[num - 1],
                result=ResultListTVP(
                    plugin_access=self,
                    value=result_value, result_quality=result_value_quality)
            )

        return StopIteration(synthesis_messages)


class AlphaMonitoringFeatureAccess(DataSourcePluginAccess):
    """
    MonitoringFeature access class
    """
    synthesis_model_class = MonitoringFeature

    def list(self, query: QueryMonitoringFeature):
        """
        Generate list of MonitoringFeature objects
        """

        feature_type = query.feature_type
        monitoring_feature_list = query.monitoring_feature

        obj_region = MonitoringFeature(
            plugin_access=self,
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
                        value=1500,
                        distance_units=VerticalCoordinate.DISTANCE_UNITS_FEET)),
                representative_point_type=RepresentativeCoordinate.REPRESENTATIVE_POINT_TYPE_CENTER_LOCAL_SURFACE)
            )
        )

        if monitoring_feature_list and 'Region1' in monitoring_feature_list:
            if feature_type == FeatureTypeEnum.REGION:
                yield obj_region
        elif feature_type == FeatureTypeEnum.REGION:
            yield obj_region

        obj_point = MonitoringFeature(
            plugin_access=self,
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
                        value=-0.5,
                        distance_units=VerticalCoordinate.DISTANCE_UNITS_METERS)
                )
            ),
            observed_properties=["Ag", "Acetate"],
            related_sampling_feature_complex=[
                RelatedSamplingFeature(
                    plugin_access=self,
                    related_sampling_feature="Region1",
                    related_sampling_feature_type=FeatureTypeEnum.REGION,
                    role=RelatedSamplingFeature.ROLE_PARENT)]
        )

        if monitoring_feature_list and '1' in monitoring_feature_list:
            if feature_type == FeatureTypeEnum.POINT:
                yield obj_point
        elif feature_type == FeatureTypeEnum.POINT:
            yield obj_point

    def get(self, query: QueryMonitoringFeature):

        """
        Get a Monitoring Feature objects
        """
        # query.id will always be a string at this point with validation upstream, thus ignoring the type checking
        prefixed_monitoring_feature = f'{self.datasource.id_prefix}-{query.id}'  # type: ignore[list-item]

        query.monitoring_feature = [query.id]  # type: ignore[list-item]

        for s in self.list(query):
            if s.id == prefixed_monitoring_feature:
                return s
        return None


@basin3d_plugin
class AlphaDataSourcePlugin(DataSourcePluginPoint):
    title = 'Alpha Data Source Plugin'
    plugin_access_classes = (AlphaMeasurementTimeseriesTVPObservationAccess, AlphaMonitoringFeatureAccess)

    feature_types = ['REGION', 'POINT', 'TREE']

    class DataSourceMeta:
        """
        This is an internal metadata class for defining DataSource attributes.
        """
        # Data Source attributes
        location = 'https://asource.foo/'
        id = 'Alpha'  # unique id for the datasource
        id_prefix = 'A'
        name = id  # Human Friendly Data Source Name
