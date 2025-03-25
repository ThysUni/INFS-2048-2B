from datetime import date
from models.transaction import Transaction
from reporting.reporting_manager import ReportingManager


class HardcodedStorage:
    def __init__(self, transactions_to_return=None):
        self.stored_transactions = []
        self.updated_labels = {}
        self.transactions_to_return = transactions_to_return or []

    def store_transactions(self, transactions):
        self.stored_transactions.extend(transactions)
        return len(transactions)

    def get_transactions(self, start_date, end_date, label=None):
        return self.transactions_to_return

    def update_transaction_label(self, transaction_id, label):
        self.updated_labels[transaction_id] = label
        return True

    def get_transaction_labels(self, start_date, end_date):
        # Return hardcoded data for the expenditure test
        return {"Food": 100.00, "Home": 1000.00, "": 25.00}


class HardcodedClassifier:
    def apply_classification_rules(self, transactions, rules_path):
        # Mark all transactions as "Food" for simplicity
        for t in transactions:
            t.set_label("Food")
        return transactions


class HardcodedReporter:
    def format_transaction_list(self, transactions):
        return ["Formatted list output"]

    def format_classification_result(self, transactions):
        return ["Formatted classification output"]

    def format_expenditure_report(self, expenditures):
        # Return the keys to check what categories are present
        result = []
        for category in expenditures:
            result.append(f"{category}: amount")
        result.append("Total: amount")
        return result


def test_import_transactions():
    # Arrange
    storage = HardcodedStorage()
    manager = ReportingManager(storage, None)

    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as temp_file:
        temp_file.write("date,description,amount\n")
        temp_file.write("2025-01-01,Test,10.00\n")
        temp_filename = temp_file.name

    # Act
    count = manager.import_transactions(temp_filename)

    # Assert
    assert count == 1
    assert len(storage.stored_transactions) == 1
    assert storage.stored_transactions[0].get_description() == "Test"


def test_classify_transactions():
    # Arrange
    storage = HardcodedStorage([
        Transaction(1, date(2025, 1, 1), "Test1", 10.00),
        Transaction(2, date(2025, 1, 2), "Test2", 20.00),
    ])
    classifier = HardcodedClassifier()
    reporter = HardcodedReporter()

    manager = ReportingManager(storage, classifier)
    manager.set_report_access(reporter)

    # Act
    result = manager.classify_transactions("dummy_path", date(2025, 1, 1), date(2025, 1, 31))

    # Assert
    assert 1 in storage.updated_labels
    assert 2 in storage.updated_labels
    assert storage.updated_labels[1] == "Food"
    assert storage.updated_labels[2] == "Food"


def test_list_transactions():
    # Arrange
    storage = HardcodedStorage()
    reporter = HardcodedReporter()

    manager = ReportingManager(storage, None)  # No classifier needed
    manager.set_report_access(reporter)

    # Act
    result = manager.list_transactions(date(2025, 1, 1), date(2025, 1, 31))

    # Assert
    assert result == ["Formatted list output"]


def test_report_expenditure_empty_label_handling():
    # Arrange
    storage = HardcodedStorage()
    reporter = HardcodedReporter()

    manager = ReportingManager(storage, None)  # No classifier needed
    manager.set_report_access(reporter)

    # Act
    result = manager.report_expenditures(date(2025, 1, 1), date(2025, 1, 31))
    categories = [line.split(":")[0] for line in result]

    assert "Food" in categories
    assert "Home" in categories
    assert "Other" in categories
    assert "" not in categories  # Empty string should be gone