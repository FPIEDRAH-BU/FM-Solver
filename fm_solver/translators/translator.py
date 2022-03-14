import abc

from fm_solver.feature_model import feature_model


class Translator(abc.ABC):
    def __init__(self, feature_model: feature_model.FeatureModel) -> None:
        self.feature_model = feature_model

    @abc.abstractmethod
    def translate(self) -> str:
        raise NotImplementedError
