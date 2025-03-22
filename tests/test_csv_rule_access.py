import pytest
from classification.csv_rule_access import CSVRuleAccess

def test_load_rules():
    # Arrange
    rule_access = CSVRuleAccess()

    # Act
    pattern_count = rule_access.load_rules("examples/patterns.csv")

    # Assert
    assert pattern_count == 20  # 20 individual patterns


def test_get_rule():
    # Arrange
    rule_access = CSVRuleAccess()

    # Act
    rule_access.load_rules("examples/patterns.csv")

    # Assert
    assert rule_access.get_rule("coffee") == "Food"
    assert rule_access.get_rule("water") == "Utilities"

    # Test case sensitivity
    assert rule_access.get_rule("Coffee") is None

    # Test a pattern that doesn't exist
    assert rule_access.get_rule("does_not_exist") is None

    # Test empty string
    assert rule_access.get_rule("") is None

#TODO
# only works when run in main folder
# if possible change it so it works from both