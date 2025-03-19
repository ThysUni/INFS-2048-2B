from datetime import date

class Transaction:
    def __init__(self, transaction_id: int, transaction_date: date, description: str, amount: float):
        self._transaction_id = transaction_id
        self._transaction_date = transaction_date
        self._description = description
        self._amount = amount
        self._label = ""

    def get_id(self):
        return self._transaction_id

    def get_date(self):
        return self._transaction_date

    def get_description(self):
        return self._description

    def get_amount(self):
        return self._amount

    def set_label(self, label):
        self._label = label

    def get_label(self):
        return self._label


