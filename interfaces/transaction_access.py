class ITransactionAccess:
    def store_transactions(self, transactions):
        pass

    def get_transactions(self, start_date, end_date, label=None):
        pass

    def update_transaction_label(self, transaction_id, label):
        pass

    def get_transaction_labels(self, start_date, end_date):
        pass