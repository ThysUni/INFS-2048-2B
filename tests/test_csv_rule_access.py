import pytest
from classification.csv_rule_access import CSVRuleAccess

def test_load_rules():
    # Arrange
    rule_access = CSVRuleAccess()

    # Act
    pattern_count = rule_access.load_rules("../examples/patterns.csv")

    # Assert
    assert pattern_count == 20  # 20 individual patterns


def test_get_rule():
    # Arrange
    rule_access = CSVRuleAccess()

    # Act
    rule_access.load_rules("../examples/patterns.csv")

    # Assert
    assert rule_access.get_rule("coffee") == "Food"
