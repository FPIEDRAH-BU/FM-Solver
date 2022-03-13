import enum
import dataclasses


@enum.unique
class Selection(str, enum.Enum):
    SELECTED = "SELECTED"
    UNSELECTED = "UNSELECTED"
    UNDEFINED = "UNDEFINED"


@dataclasses.dataclass
class Feature:
    identifier: int
    name: str
    selection: Selection = Selection.UNDEFINED
