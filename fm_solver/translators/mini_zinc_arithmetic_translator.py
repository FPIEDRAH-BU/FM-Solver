import functools
import typing

from fm_solver import feature_model
from fm_solver.translators import translator


class MiniZincArithmeticTranslator(translator.Translator):
    def translate(self):
        csp = []

        for feature in self.feature_model.features.values():
            csp.append(self.translate_feature(feature))

        for restriction in self.feature_model.restrictions:
            csp.append(self.translate_restriction(restriction))

        return "\n".join(csp)

    def translate_feature(self, feature: feature_model.Feature) -> str:
        if feature.selection == feature_model.Selection.SELECTED:
            return f"var 0..1: feature_{feature.identifier} = 1;"

        if feature.selection == feature_model.Selection.UNSELECTED:
            return f"var 0..1: feature{feature.identifier} = 0;"

        return f"var 0..1: feature_{feature.identifier};"

    @functools.singledispatchmethod
    def translate_restriction(self, restriction) -> str:
        raise NotImplementedError

    @translate_restriction.register
    def _(self, restriction: feature_model.Root) -> str:
        return f"constraint (feature_{restriction.source.identifier} == 1);"

    @translate_restriction.register
    def _(self, restriction: feature_model.Mandatory) -> str:
        return (
            f"constraint (feature_{restriction.source.identifier} "
            + f"== feature_{restriction.destination[0].identifier});"
        )

    @translate_restriction.register
    def _(self, restriction: feature_model.Optional) -> str:
        return (
            f"constraint (feature_{restriction.destination[0].identifier} "
            + f"<= feature_{restriction.source.identifier});"
        )

    @translate_restriction.register
    def _(self, restriction: feature_model.Requires) -> str:
        return (
            f"constraint (((1 - feature_{restriction.source.identifier}) "
            + f"+ feature_{restriction.destination[0].identifier}) >= 0);"
        )

    @translate_restriction.register
    def _(self, restriction: feature_model.Excludes) -> str:
        return (
            f"constraint (feature_{restriction.source.identifier} "
            + f"* feature_{restriction.destination[0].identifier} > 0);"
        )

    def build_cardinality_restriction(
        self,
        restriction: typing.Union[
            feature_model.And, feature_model.Or, feature_model.Xor, feature_model.Range
        ],
    ) -> str:
        return (
            f"feature_{restriction.source.identifier} * {restriction.cardinality.lower_bound} <= "
            + " + ".join(
                [
                    f"feature_{restriction.identifier}"
                    for restriction in restriction.destination
                ]
            )
            + f" <= feature_{restriction.source.identifier} * {restriction.cardinality.upper_bound}"
        )

    @translate_restriction.register
    def _(self, restriction: feature_model.And) -> str:
        return self.build_cardinality_restriction(restriction)

    @translate_restriction.register
    def _(self, restriction: feature_model.Or) -> str:
        return self.build_cardinality_restriction(restriction)

    @translate_restriction.register
    def _(self, restriction: feature_model.Xor) -> str:
        return self.build_cardinality_restriction(restriction)

    def _(self, restriction: feature_model.Range) -> str:
        return self.build_cardinality_restriction(restriction)
