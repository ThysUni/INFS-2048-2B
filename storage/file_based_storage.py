import json
from datetime import date
from models.transaction import Transaction
from interfaces.transaction_access import ITransactionAccess


class FileBasedStorage(ITransactionAccess):
    def __init__(self, internal_storage="transactions.json"):
        """
        Initialize the storage with a file path
        """
        self._internal_storage = internal_storage
        self._transactions = []
        try:
            self._load_transactions()
        except Exception as e:
            print(f"Error loading transactions: {e}")
            self._transactions = []

    def _load_transactions(self):
        """
        Reads the JSON file and converts the data into Transaction objects
        """
        try:
            with open(self._internal_storage, 'r') as json_file:
                data = json.load(json_file)
                self._transactions = []
                for t in data:
                    transaction = Transaction(
                        t["id"],
                        date.fromisoformat(t["date"]),
                        t["description"],
                        t["amount"]
                    )
                    if "label" in t:
                        transaction.set_label(t["label"])
                    self._transactions.append(transaction)
        except FileNotFoundError:
            # File doesn't exist yet, start with empty list
            self._transactions = []
        except json.JSONDecodeError:
            # File exists but isn't valid JSON, start with empty list
            self._transactions = []

    def _save_transactions(self):
        """
        Converts Transaction objects to dictionaries and saves to JSON file
        """
        data = []
        for t in self._transactions:
            transaction_dict = {
                "id": t.get_id(),
                "date": t.get_date().isoformat(),
                "description": t.get_description(),
                "amount": t.get_amount(),
                "label": t.get_label()
            }
            data.append(transaction_dict)

        with open(self._internal_storage, 'w') as json_file:
            json.dump(data, json_file)

    def store_transactions(self, transactions):
        """
        Adds new transactions to storage
        """
        next_id = 1
        if self._transactions:
            ids = [t.get_id() for t in self._transactions if t.get_id() is not None]
            if ids:
                next_id = max(ids) + 1

        added_transactions = []
        for t in transactions:
            if t.get_id() is None:
                # Create a new Transaction with the assigned ID
                new_transaction = Transaction(
                    next_id,
                    t.get_date(),
                    t.get_description(),
                    t.get_amount()
                )
                new_transaction.set_label(t.get_label())
                next_id += 1
                added_transactions.append(new_transaction)
            else:
                added_transactions.append(t)

        # Add the new transactions to list
        self._transactions.extend(added_transactions)

        # Save the updated transactions
        self._save_transactions()

        return len(transactions)

    def get_transactions(self, start_date, end_date, label=None):
        """
        Retrieves transactions in the given date range with the optional label
        """
        # Make sure we have the latest data
        self._load_transactions()

        result = []
        for t in self._transactions:
            transaction_date = t.get_date()
            if start_date <= transaction_date <= end_date:
                if label is None or t.get_label() == label:
                    result.append(t)

        return result

    def update_transaction_label(self, transaction_id, label):
        """
        Updates the label of a specific transaction
        """
        # Make sure we have the latest data
        self._load_transactions()

        for t in self._transactions:
            if t.get_id() == transaction_id:
                t.set_label(label)
                self._save_transactions()
                return True

        return False

    def get_transaction_labels(self, start_date, end_date):
        """
        Calculates the total amount for each label within a date range
        """
        # Make sure we have the latest data
        self._load_transactions()

        result = {}
        for t in self._transactions:
            if start_date <= t.get_date() <= end_date:
                label = t.get_label()
                if label not in result:
                    result[label] = 0
                result[label] += t.get_amount()

        return result