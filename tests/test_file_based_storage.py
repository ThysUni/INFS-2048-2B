import pytest
from datetime import date
from models.transaction import Transaction
from storage.file_based_storage import FileBasedStorage


@pytest.fixture
def sample_transactions():
    return [
        Transaction(None, date(2023, 1, 1), "Coffee", 6.50),
        Transaction(None, date(2023, 1, 2), "Rent", 1000.00),
        Transaction(None, date(2023, 1, 3), "Coffee", 5.50)
    ]


def test_store_and_retrieve_transactions(sample_transactions):
    test_file = "test_transactions_1.json"
    storage = FileBasedStorage(test_file)

    # Store transactions (just using the first two)
    count = storage.store_transactions(sample_transactions[:2])
    assert count == 2

    retrieved = storage.get_transactions(date(2023, 1, 1), date(2023, 1, 31))
    assert len(retrieved) == 2
    assert retrieved[0].get_description() == "Coffee"
    assert retrieved[1].get_description() == "Rent"


def test_update_transaction_label(sample_transactions):
    test_file = "test_transactions_2.json"
    storage = FileBasedStorage(test_file)

    # Create and store a transaction (just using the first one)
    storage.store_transactions([sample_transactions[0]])
    retrieved = storage.get_transactions(date(2023, 1, 1), date(2023, 1, 31))
    assert len(retrieved) == 1

    transaction_id = retrieved[0].get_id()
    result = storage.update_transaction_label(transaction_id, "Food")
    assert result is True

    updated = storage.get_transactions(date(2023, 1, 1), date(2023, 1, 31))
    assert updated[0].get_label() == "Food"


def test_get_transaction_labels(sample_transactions):
    test_file = "test_transactions_3.json"
    storage = FileBasedStorage(test_file)

    # Store all three transactions
    storage.store_transactions(sample_transactions)
    retrieved = storage.get_transactions(date(2023, 1, 1), date(2023, 1, 31))

    storage.update_transaction_label(retrieved[0].get_id(), "Food")
    storage.update_transaction_label(retrieved[1].get_id(), "Home")
    storage.update_transaction_label(retrieved[2].get_id(), "Food")

    labels = storage.get_transaction_labels(date(2023, 1, 1), date(2023, 1, 31))
    assert len(labels) == 2
    assert labels["Food"] == 12.00
    assert labels["Home"] == 1000.00

# TODO
# have a simple clean way to remove test_transactions JSNO files after use.
# ignore: Error loading transactions, test does work, file not there "yet"