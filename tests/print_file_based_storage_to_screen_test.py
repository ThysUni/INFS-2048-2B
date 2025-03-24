from datetime import date
from models.transaction import Transaction
from storage.file_based_storage import FileBasedStorage


def print_file_based_storage_contents():
    storage = FileBasedStorage("print_test_transactions.json")

    # Create some sample transactions
    transactions = [
        Transaction(None, date(2025, 1, 1), "Morning Coffee", 6.50),
        Transaction(None, date(2025, 1, 5), "Lunch at Cafe", 22.50),
        Transaction(None, date(2025, 1, 10), "Monthly Rent", 1000.00),
        Transaction(None, date(2025, 1, 15), "Electric Bill", 85.75),
    ]

    # Store transactions
    storage.store_transactions(transactions)

    # Get and print all transactions
    all_transactions = storage.get_transactions(date(2025, 1, 1), date(2025, 1, 31))
    print('\n' + '-' * 50)
    for t in all_transactions:
        print(t.get_date().isoformat(), "|", t.get_description(), "|", t.get_amount())

    # Set some labels
    retrieved = storage.get_transactions(date(2025, 1, 1), date(2025, 1, 31))
    storage.update_transaction_label(retrieved[0].get_id(), "Food")
    storage.update_transaction_label(retrieved[1].get_id(), "Food")
    storage.update_transaction_label(retrieved[2].get_id(), "Home")
    storage.update_transaction_label(retrieved[3].get_id(), "Utilities")

    # Print expenditure report
    label_totals = storage.get_transaction_labels(date(2025, 1, 1), date(2025, 1, 31))
    print('\n' + '-' * 50)
    for label in label_totals:
        print(label + ":", label_totals[label])

# TODO
# remove temp print_test_transactions.json after use

if __name__ == "__main__":
    print_file_based_storage_contents()

