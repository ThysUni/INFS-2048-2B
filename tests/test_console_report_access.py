import pytest
from datetime import date
from models.transaction import Transaction
from reporting.console_report_access import ConsoleReportAccess

@pytest.fixture()
def sample_transaction():
    transactions = [
        Transaction(1, date(2025, 3, 23), "Coffee", 6.50),
        Transaction(2, date(2025, 3, 22), "Rent", 1000.00),
    ]

    transactions[0].set_label("Food")
    # leave 2nd one without label

    return transactions

@pytest.fixture()
def sample_expenditure():
    expenditures = {
        "Food": 150.75,
        "Home": 1000.00,
        "Utilities": 75.50,
        "": 25.00
    }

    return expenditures

def test_format_transaction_list(sample_transaction):
    # Arrange
    report_access = ConsoleReportAccess()

    # Act
    result = report_access.format_transaction_list(sample_transaction)

    # Assert
    assert len(result) == 3  # 2 transactions + summary line
    assert result[0] == "2025-03-23 Coffee: 6.50 [Food]"
    assert result[1] == "2025-03-22 Rent: 1000.00 []"
    assert result[2] == "2 transaction(s) listed"

def test_format_classification_result(sample_transaction):
    # Arrange
    report_access = ConsoleReportAccess()

    # Act
    result = report_access.format_classification_result(sample_transaction)

    # Assert
    assert result[0] == "2025-03-23 Coffee: 6.50 classified as Food"
    assert result[1] == "2025-03-22 Rent: 1000.00 unable to classify"
    assert result[2] == "2 transaction(s) processed"

def test_format_expenditure_report(sample_expenditure):
    # Arrange
    report_access = ConsoleReportAccess()

    # Act
    result = report_access.format_expenditure_report(sample_expenditure)

    # Assert
    assert len(result) == 5 # 4 categories + total
    assert "Food: 150.75" in result
    assert "Other: 25.00" in result
    assert "Total: 1251.25" in result