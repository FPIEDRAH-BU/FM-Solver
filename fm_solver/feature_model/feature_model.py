import typing

from fm_solver.feature_model import feature, restriction


class FeatureModel:
    def __init__(
        self,
        features: typing.List[feature.Feature],
        restrictions: typing.List[restriction.Restriction],
    ) -> None:
        self.features = {feature.identifier: feature for feature in features}
        self.restrictions = restrictions

    def get_feature(self, identifier: int) -> typing.Optional[feature.Feature]:
        return self.features.get(identifier)

    def add_feature(self, feature: feature.Feature) -> None:
        if feature.identifier in self.features:
            return ValueError(f"Feature with id: {feature.identifier} already exist.")

        self.features[feature.identifier] = feature

    def add_features(self, features: typing.List[feature.Feature]) -> None:
        for feature in features:
            self.add_feature(feature)

    def change_feature_selection(
        self, feature_id: int, selection: feature.Selection
    ) -> None:
        if feature_id in self.features:
            return ValueError(f"No feature with id {feature_id} exists.")

        self.features[feature_id].selection = selection

    def add_restriction(self, restriction: restriction.Restriction) -> None:
        self.restrictions.append(restriction)

    def add_restrictions(
        self, restrictions: typing.List[restriction.Restriction]
    ) -> None:
        for restriction in restrictions:
            self.add_restriction(restriction)

    def get_restrictions_with_source(
        self, feature: feature.Feature,
    ) -> typing.List[restriction.Restriction]:
        return [
            restriction
            for restriction in self.restrictions
            if feature == restriction.source
        ]

    def get_restrictions_with_destination(
        self, feature: feature
    ) -> typing.List[restriction.Restriction]:
        return [
            restriction
            for restriction in self.restrictions
            if feature in restriction.destination
        ]
