import dataclasses
import typing

from fm_solver.feature_model import feature


@dataclasses.dataclass
class Cardinality:
    lower_bound: int
    upper_bound: int


@dataclasses.dataclass
class Restriction:
    source: typing.Optional[feature.Feature]
    destination: typing.Optional[typing.List[feature.Feature]]
    cardinality: Cardinality


class Root(Restriction):
    def __init__(self, source: feature.Feature) -> None:
        super().__init__(
            source=source,
            destination=[source],
            cardinality=Cardinality(lower_bound=1, upper_bound=1),
        )


class Mandatory(Restriction):
    def __init__(self, source: feature.Feature, destination: feature.Feature) -> None:
        super().__init__(
            source=source,
            destination=[destination],
            cardinality=Cardinality(lower_bound=1, upper_bound=1),
        )


class Optional(Restriction):
    def __init__(self, source: feature.Feature, destination: feature.Feature) -> None:
        super().__init__(
            source=source,
            destination=[destination],
            cardinality=Cardinality(lower_bound=1, upper_bound=1),
        )


class Requires(Restriction):
    def __init__(self, source: feature.Feature, destination: feature.Feature) -> None:
        super().__init__(
            source=source,
            destination=[destination],
            cardinality=Cardinality(lower_bound=1, upper_bound=1),
        )


class Excludes(Restriction):
    def __init__(self, source: feature.Feature, destination: feature.Feature) -> None:
        super().__init__(
            source=source,
            destination=[destination],
            cardinality=Cardinality(lower_bound=1, upper_bound=1),
        )


class And(Restriction):
    def __init__(
        self, source: feature.Feature, destination: typing.List[feature.Feature]
    ) -> None:
        super().__init__(
            source=source,
            destination=destination,
            cardinality=Cardinality(
                lower_bound=len(destination), upper_bound=len(destination)
            ),
        )


class Or(Restriction):
    def __init__(
        self, source: feature.Feature, destination: typing.List[feature.Feature]
    ) -> None:
        super().__init__(
            source=source,
            destination=destination,
            cardinality=Cardinality(lower_bound=1, upper_bound=len(destination)),
        )


class Xor(Restriction):
    def __init__(
        self, source: feature.Feature, destination: typing.List[feature.Feature]
    ) -> None:
        super().__init__(
            source=source,
            destination=destination,
            cardinality=Cardinality(lower_bound=1, upper_bound=1),
        )


class Range(Restriction):
    def __init__(
        self,
        source: feature.Feature,
        destination: typing.List[feature.Feature],
        cardinality: Cardinality,
    ) -> None:
        super().__init__(
            source=source, destination=destination, cardinality=cardinality
        )
