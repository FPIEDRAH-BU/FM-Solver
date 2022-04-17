import functools
import typing

from lxml import etree
from lxml.builder import E

from fm_solver import feature_model
from fm_solver.translator import translator


class XCSP3ArithmeticTranslator(translator.Translator):
    def translate(self):
        variables = [
            self.translate_feature(feature)
            for feature in self.feature_model.features.values()
        ]

        constraints = [
            self.translate_restriction(restriction)
            for restriction in self.feature_model.restrictions
        ]

        csp = E.instance(E.variables(*variables), E.constraints(*constraints))

        return etree.tostring(csp, pretty_print=True).decode("utf-8")

    def translate_feature(self, feature: feature_model.Feature):
        return E.var("0 1", id=f"feature_{feature.identifier}")

    @functools.singledispatchmethod
    def translate_restriction(self, restriction):
        raise NotImplementedError

    @translate_restriction.register
    def _(self, restriction: feature_model.Root):
        return E.intension(f"eq(feature_{restriction.source.identifier}, 1)")

    @translate_restriction.register
    def _(self, restriction: feature_model.Mandatory):
        source = f"feature_{restriction.source.identifier}"
        destination = f"feature_{restriction.destination[0].identifier}"

        return E.intension(f"eq({source}, {destination})")

    @translate_restriction.register
    def _(self, restriction: feature_model.Optional):
        source = f"feature_{restriction.source.identifier}"
        destination = f"feature_{restriction.destination[0].identifier}"

        return E.intension(f"le({source}, {destination})")

    @translate_restriction.register
    def _(self, restriction: feature_model.Requires):
        source = f"feature_{restriction.source.identifier}"
        destination = f"feature_{restriction.destination[0].identifier}"

        return E.intension(f"gt((1 - {source}) + {destination}, 0)")

    @translate_restriction.register
    def _(self, restriction: feature_model.Excludes):
        source = f"feature_{restriction.source.identifier}"
        destination = f"feature_{restriction.destination[0].identifier}"

        return E.intension(f"gt({source} * {destination}, 0)")

    def build_cardinality_restriction(
        self,
        restriction: typing.Union[
            feature_model.And, feature_model.Or, feature_model.Xor, feature_model.Range
        ],
    ):
        source = f"feature_{restriction.source.identifier}"
        destination_sum = " + ".join(
            [
                f"feature_{restriction.identifier}"
                for restriction in restriction.destination
            ]
        )

        cardinality_1 = (
            f"le({source} * {restriction.cardinality.lower_bound}, ({destination_sum}))"
        )
        cardinality_2 = (
            f"le(({destination_sum}), {source} * {restriction.cardinality.upper_bound})"
        )

        return E.intension(f"and({cardinality_1}, {cardinality_2})")

    @translate_restriction.register
    def _(self, restriction: feature_model.And):
        return self.build_cardinality_restriction(restriction)

    @translate_restriction.register
    def _(self, restriction: feature_model.Or):
        return self.build_cardinality_restriction(restriction)

    @translate_restriction.register
    def _(self, restriction: feature_model.Xor):
        return self.build_cardinality_restriction(restriction)

    def _(self, restriction: feature_model.Range):
        return self.build_cardinality_restriction(restriction)
