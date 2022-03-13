import pytest

from fm_solver.feature_model import feature, restriction


@pytest.fixture
def single_source():
    return feature.Feature(identifier=1, name="feature_1")


@pytest.fixture
def single_destination():
    return feature.Feature(identifier=2, name="feature_2")


@pytest.fixture
def multiple_destination():
    return [
        feature.Feature(identifier=2, name="feature_2"),
        feature.Feature(identifier=3, name="feature_3"),
        feature.Feature(identifier=4, name="feature_4"),
    ]


def test_restriction():
    restriction_instance = restriction.Restriction(
        source=None,
        destination=None,
        cardinality=restriction.Cardinality(lower_bound=1, upper_bound=1),
    )

    assert restriction_instance.source is None
    assert restriction_instance.destination is None
    assert restriction_instance.cardinality.lower_bound == 1
    assert restriction_instance.cardinality.upper_bound == 1


def test_root(single_source):
    restriction_instance = restriction.Root(source=single_source)

    assert restriction_instance.source == single_source
    assert restriction_instance.destination[0] == single_source
    assert restriction_instance.cardinality.lower_bound == 1
    assert restriction_instance.cardinality.upper_bound == 1


def test_mandatory(single_source, single_destination):
    restriction_instance = restriction.Mandatory(
        source=single_source, destination=single_destination,
    )

    assert restriction_instance.source == single_source
    assert restriction_instance.destination[0] == single_destination
    assert restriction_instance.cardinality.lower_bound == 1
    assert restriction_instance.cardinality.upper_bound == 1


def test_requires(single_source, single_destination):
    restriction_instance = restriction.Requires(
        source=single_source, destination=single_destination,
    )

    assert restriction_instance.source == single_source
    assert restriction_instance.destination[0] == single_destination
    assert restriction_instance.cardinality.lower_bound == 1
    assert restriction_instance.cardinality.upper_bound == 1


def test_excludes(single_source, single_destination):
    restriction_instance = restriction.Excludes(
        source=single_source, destination=single_destination,
    )

    assert restriction_instance.source == single_source
    assert restriction_instance.destination[0] == single_destination
    assert restriction_instance.cardinality.lower_bound == 1
    assert restriction_instance.cardinality.upper_bound == 1


def test_and(single_source, multiple_destination):
    restriction_instance = restriction.And(
        source=single_source, destination=multiple_destination
    )

    assert restriction_instance.source == single_source
    assert restriction_instance.destination == multiple_destination
    assert restriction_instance.cardinality.lower_bound == 3
    assert restriction_instance.cardinality.upper_bound == 3


def test_or(single_source, multiple_destination):
    restriction_instance = restriction.Or(
        source=single_source, destination=multiple_destination
    )

    assert restriction_instance.source == single_source
    assert restriction_instance.destination == multiple_destination
    assert restriction_instance.cardinality.lower_bound == 1
    assert restriction_instance.cardinality.upper_bound == 3


def test_xor(single_source, multiple_destination):
    restriction_instance = restriction.Xor(
        source=single_source, destination=multiple_destination
    )

    assert restriction_instance.source == single_source
    assert restriction_instance.destination == multiple_destination
    assert restriction_instance.cardinality.lower_bound == 1
    assert restriction_instance.cardinality.upper_bound == 1


def test_range(single_source, multiple_destination):
    restriction_instance = restriction.Range(
        source=single_source,
        destination=multiple_destination,
        cardinality=restriction.Cardinality(lower_bound=1, upper_bound=2),
    )

    assert restriction_instance.source == single_source
    assert restriction_instance.destination == multiple_destination
    assert restriction_instance.cardinality.lower_bound == 1
    assert restriction_instance.cardinality.upper_bound == 2
