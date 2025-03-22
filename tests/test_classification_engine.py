from datetime import date
from models.transaction import Transaction
from classification.classification_engine import ClassificationEngine


class MockRuleAccess:
    def __init__(self):
        self._rules_cache = {}

    def load_rules(self, filepath):
        # Simulate loading rules by hard coding instead of reading actual file
        self._rules_cache = {
            "coffee": "Food",
            "rent": "Home",
            "power": "Utilities"
        }
        return len(self._rules_cache)

    def get_rule(self, pattern):
        return self._rules_cache.get(pattern)


def test_apply_classification_rules():
    # Arrange
    mock_rule_access = MockRuleAccess()
    engine = ClassificationEngine(mock_rule_access)

    transactions = [
        Transaction(1, date(2025, 3, 1), "Take Away coffee", 6.50),
        Transaction(2, date(2025, 3, 2), "Monthly rent", 1000.00),
        Transaction(3, date(2025, 3, 3), "Power bill", 150.00),
        Transaction(4, date(2025, 3, 4), "Unknown transaction", 25.00)
    ]

    # Act
    classified = engine.apply_classification_rules(transactions, "dummy_path")

    # Assert
    assert classified[0].get_label() == "Food"
    assert classified[1].get_label() == "Home"
    assert classified[2].get_label() == "Utilities"
    assert classified[3].get_label() == ""  # Should remain unclassified



