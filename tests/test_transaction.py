from datetime import date
from models.transaction import Transaction


def test_transaction_creation():
    # Arrange
    transaction_id = 1
    transaction_date = date(2025, 3, 18)
    description = "Soy Latte"
    amount = 5.50

    # Act
    transaction = Transaction(transaction_id, transaction_date, description, amount)

    # Assert
    assert transaction.get_id() == transaction_id
    assert transaction.get_date() == transaction_date
    assert transaction.get_description() == description
    assert transaction.get_amount() == amount
    assert transaction.get_label() == ""

def test_transaction_label():
    # Arrange
    transaction = Transaction(1, date(2025, 3, 18), "Large Latte", 6.50)

    # Act
    transaction.set_label("Food")

    # Assert
    assert transaction.get_label() == "Food"


