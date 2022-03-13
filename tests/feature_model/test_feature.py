from fm_solver.feature_model import feature


def test_selection_selected():
    assert feature.Selection.SELECTED.value == "SELECTED"


def test_selection_unselected():
    assert feature.Selection.UNSELECTED.value == "UNSELECTED"


def test_selection_undefined():
    assert feature.Selection.UNDEFINED.value == "UNDEFINED"


def test_feature_default_selection():
    feature_instance = feature.Feature(identifier=1, name="feature_1")

    assert feature_instance.identifier == 1
    assert feature_instance.name == "feature_1"
    assert feature_instance.selection == feature.Selection.UNDEFINED
