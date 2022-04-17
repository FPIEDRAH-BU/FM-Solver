import collections, random, typing

from fm_solver.feature_model import feature, feature_model, restriction


def _restriction_amounts(
    feature_amount: int,
    mandatory_weight: float = 0.25,
    optional_weight: float = 0.25,
    or_weight: float = 0.25,
    xor_weight: float = 0.25,
):
    restrictions = random.choices(
        population=[
            restriction.Mandatory,
            restriction.Optional,
            restriction.Or,
            restriction.Xor,
        ],
        weights=[mandatory_weight, optional_weight, or_weight, xor_weight],
        k=feature_amount,
    )

    return collections.Counter(restrictions)


def _cross_tree_restriction_amounts(
    restriction_amount: int,
    requires_weight: float = 0.5,
    excludes_weight: float = 0.5,
):
    restrictions = random.choices(
        population=[
            restriction.Requires,
            restriction.Excludes,
        ],
        weights=[requires_weight, excludes_weight],
        k=restriction_amount,
    )

    return collections.Counter(restrictions)


def _build_features(starting_indentifier: int, feature_amount: int):
    start = starting_indentifier + 1
    end = starting_indentifier + feature_amount + 1

    return [
        feature.Feature(identifier, f"feature_{identifier}")
        for identifier in range(start, end)
    ]


def _build_restrictions(
    father: feature.Feature,
    features: typing.List[feature.Feature],
    restriction_counts: typing.Dict[typing.Type[restriction.Restriction], int],
) -> typing.List[restriction.Restriction]:
    last_index, restrictions = 0, []

    for restriction_class, amount in restriction_counts.items():
        children = features[last_index : last_index + amount]

        if (
            restriction_class == restriction.Mandatory
            or restriction_class == restriction.Optional
        ):
            for child in children:
                restrictions.append(restriction_class(source=father, destination=child))
        else:
            restrictions.append(restriction_class(source=father, destination=children))

    return restrictions


def _build_cross_tree_restrictions(
    model: feature_model.FeatureModel,
    cross_tree_restriction_count: typing.Dict[
        typing.Type[restriction.Restriction], int
    ],
) -> typing.List[restriction.Restriction]:
    restrictions = []

    for restriction_class, amount in cross_tree_restriction_count.items():
        for _ in range(amount):
            source, destination = random.sample(model.features.items(), 2)
            restrictions.append(
                restriction_class(source=source, destination=destination)
            )

    return restrictions


def random_feature_model(
    size: int,
    cross_tree_restriction_amount: int,
    min_feantures: int = 1,
    max_features: int = 10,
    mandatory_weight: float = 0.25,
    optional_weight: float = 0.25,
    or_weight: float = 0.25,
    xor_weight: float = 0.25,
    requires_weight: float = 0.5,
    excludes_weight: float = 0.5,
):
    root = feature.Feature(identifier=1, name="feature_1")
    root_restriction = restriction.Root(source=root)

    childless = [root]
    model = feature_model.FeatureModel([root], [root_restriction])

    while len(model.features) < size:
        father = childless.pop()
        starting_indentifier = len(model.features) + 1
        feature_amount = random.randint(min_feantures, max_features)
        restriction_counts = _restriction_amounts(
            feature_amount=feature_amount,
            mandatory_weight=mandatory_weight,
            optional_weight=optional_weight,
            or_weight=or_weight,
            xor_weight=xor_weight,
        )
        features = _build_features(
            starting_indentifier=starting_indentifier, feature_amount=feature_amount
        )
        restrictions = _build_restrictions(
            father=father,
            features=features,
            restriction_counts=restriction_counts,
        )

        model.add_features(features)
        model.add_restrictions(restrictions)

        childless.extend(features)

    restriction_counts = _cross_tree_restriction_amounts(
        restriction_amount=cross_tree_restriction_amount,
        requires_weight=requires_weight,
        excludes_weight=excludes_weight,
    )
    restrictions = _build_cross_tree_restrictions(
        model=model, cross_tree_restriction_count=restriction_counts
    )

    model.add_restrictions(restrictions)

    return model
