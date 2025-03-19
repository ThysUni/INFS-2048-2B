from datetime import date

class Transaction:
    def __init__(self, transaction_id, transaction_date, description, amount):
        self.transaction_id = transaction_id
        self.transaction_date = transaction_date
        self.description = description
        self.amount = amount
        self._label = ""

    def get_id(self):
        return self.transaction_id

    def get_date(self):
        return self.transaction_date

    def get_description(self):
        return self.description

    def get_amount(self):
        return self.amount

    def set_label(self, label):
        self._label = label

    def get_label(self):
        return self._label


