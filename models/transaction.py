from datetime import date

class Transaction:
    def __init__(self, transaction_id, transaction_date, description, amount):
        self.transaction_id = transaction_id
        self.transaction_date = transaction_date
        self.description = description
        self.amount = amount
