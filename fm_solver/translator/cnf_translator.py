import functools
import typing

from sympy import symbols, true, false
from sympy.core.symbol import Symbol
from sympy.logic.boolalg import (
    And,
    Or,
    Not,
    Xor,
    Nand,
    Nor,
    Xnor,
    Implies,
    Equivalent,
    to_cnf,
)

from fm_solver import feature_model
from fm_solver.translator import translator


class DimacsMapping:
    def __init__(self):
        self._symbol_to_variable = {}
        self._variable_to_symbol = {}
        self._total_variables = 0

    @property
    def total_variables(self):
        return self._total_variables

    def new_variable(self):
        self._total_variables += 1
        return self._total_variables

    def get_variable_for(self, symbol):
        result = self._symbol_to_variable.get(symbol)
        if result is None:
            result = self.new_variable()

            self._symbol_to_variable[symbol] = result
            self._variable_to_symbol[result] = symbol

        return result

    def get_symbol_for(self, variable):
        self._variable_to_symbol[variable]

    def __str__(self) -> str:
        return str(self._variable_to_symbol)


class DimacsFormula:
    def __init__(self, mapping, clauses):
        self._mapping = mapping
        self._clauses = clauses

    @property
    def mapping(self):
        return self._mapping

    @property
    def clauses(self):
        return self._clauses

    def __str__(self):
        header = f"p cnf {self._mapping.total_variables} {len(self._clauses)}"
        body = "\n".join(
            " ".join([str(literal) for literal in clause] + ["0"])
            for clause in self._clauses
        )

        return "\n".join([header, body])


def to_dimacs_formula(sympy_cnf):
    dimacs_mapping = DimacsMapping()
    dimacs_clauses = []

    assert type(sympy_cnf) == And
    for sympy_clause in sympy_cnf.args:
        dimacs_clause = []
        if type(sympy_clause) == Symbol:
            sympy_symbol, polarity = sympy_clause, 1

            dimacs_variable = dimacs_mapping.get_variable_for(sympy_symbol)
            dimacs_literal = dimacs_variable * polarity
            dimacs_clause.append(dimacs_literal)
        elif type(sympy_clause) == Or:
            for sympy_literal in sympy_clause.args:
                if type(sympy_literal) == Not:
                    sympy_symbol, polarity = sympy_literal.args[0], -1
                elif type(sympy_literal) == Symbol:
                    sympy_symbol, polarity = sympy_literal, 1
                else:
                    raise AssertionError("invalid cnf")

                dimacs_variable = dimacs_mapping.get_variable_for(sympy_symbol)
                dimacs_literal = dimacs_variable * polarity
                dimacs_clause.append(dimacs_literal)

        dimacs_clauses.append(dimacs_clause)

    return DimacsFormula(dimacs_mapping, dimacs_clauses)


class CNFTranslator(translator.Translator):
    def translate(self):
        self._features = {
            feature.name: feature
            for feature in map(
                lambda feature: self.translate_feature(feature),
                self.feature_model.features.values(),
            )
        }

        cnf = to_cnf(
            And(
                *[
                    self.translate_restriction(restriction)
                    for restriction in self.feature_model.restrictions
                ]
            )
        )

        return str(to_dimacs_formula(cnf))

    def translate_feature(self, feature: feature_model.Feature):
        return symbols(f"feature_{feature.identifier}")

    @functools.singledispatchmethod
    def translate_restriction(self, restriction):
        raise NotImplementedError

    @translate_restriction.register
    def _(self, restriction: feature_model.Root):
        source = self._features[f"feature_{restriction.source.identifier}"]

        return Equivalent(source, true)

    @translate_restriction.register
    def _(self, restriction: feature_model.Mandatory):
        source = self._features[f"feature_{restriction.source.identifier}"]
        destination = self._features[f"feature_{restriction.destination[0].identifier}"]

        return Equivalent(source, destination)

    @translate_restriction.register
    def _(self, restriction: feature_model.Optional):
        source = self._features[f"feature_{restriction.source.identifier}"]
        destination = self._features[f"feature_{restriction.destination[0].identifier}"]

        return Implies(destination, source)

    @translate_restriction.register
    def _(self, restriction: feature_model.Requires):
        source = self._features[f"feature_{restriction.source.identifier}"]
        destination = self._features[f"feature_{restriction.destination[0].identifier}"]

        return Implies(source, destination)

    @translate_restriction.register
    def _(self, restriction: feature_model.Excludes):
        source = self._features[f"feature_{restriction.source.identifier}"]
        destination = self._features[f"feature_{restriction.destination[0].identifier}"]

        return Not(And(source, destination))

    @translate_restriction.register
    def _(self, restriction: feature_model.And) -> str:
        source = self._features[f"feature_{restriction.source.identifier}"]
        destination = [
            self._features[f"feature_{feature.identifier}"]
            for feature in restriction.destination
        ]

        return Equivalent(source, And(*destination))

    @translate_restriction.register
    def _(self, restriction: feature_model.Or) -> str:
        source = self._features[f"feature_{restriction.source.identifier}"]
        destination = [
            self._features[f"feature_{feature.identifier}"]
            for feature in restriction.destination
        ]

        return Equivalent(source, Or(*destination))

    @translate_restriction.register
    def _(self, restriction: feature_model.Xor) -> str:
        source = self._features[f"feature_{restriction.source.identifier}"]
        destination = [
            self._features[f"feature_{feature.identifier}"]
            for feature in restriction.destination
        ]

        return Equivalent(source, Xor(*destination))

    # TODO: Implement Range on CNF
    @translate_restriction.register
    def _(self, restriction: feature_model.Range) -> str:
        raise NotImplementedError
