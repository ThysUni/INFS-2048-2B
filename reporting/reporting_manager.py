import csv
from datetime import date
from models.transaction import Transaction


class ReportingManager:
    def __init__(self, transaction_access, classification_engine):
        self._transaction_access = transaction_access
        self._classification_engine = classification_engine
        self._report_access = None

    def set_report_access(self, report_access):
        self._report_access = report_access

    def import_transactions(self, filepath):
        """
        Import Transactions - opens and reads the CSV file with transaction data
        :param filepath:
        :return: count of transactions imported
        """
        transactions = []
        with open(filepath, 'r') as csv_file:
            reader = csv.reader(csv_file)
            next(reader)
            for row in reader:
                if len(row) >= 3: # making sure we have all required fields
                    transaction_date_str, description, amount = row[0], row[1], row[2]

                    # date format conversion
                    if '/' in transaction_date_str:
                        # assuming DD/MM/YYYY format
                        day, month, year = transaction_date_str.split('/')
                        # convert to YYYY-MM-DD
                        transaction_date = f"{year}-{month}-{day}"

                    try:
                        transaction_date = date.fromisoformat(transaction_date_str)

                        t = Transaction(
                            None,
                            transaction_date,
                            description,
                            float(amount)
                        )
                        transactions.append(t)
                    except ValueError as e:
                        print(f"Waring: could not parse date: '{transaction_date_str}': {e}. Skipping.")
                        continue

        count = self._transaction_access.store_transactions(transactions)
        return count

    def classify_transactions(self, rules_path, start_date, end_date):
        """
        Classify Transactions  - Gets transactions for the specified date range
        :return: formats the results for display or returns classified transactions
        """
        transactions = self._transaction_access.get_transactions(start_date, end_date)
        classified = self._classification_engine.apply_classification_rules(transactions, rules_path)

        for t in classified:
            self._transaction_access.update_transaction_label(t.get_id(), t.get_label())

        if self._report_access:
            return self._report_access.format_classification_result(classified)
        return classified

    def list_transactions(self, start_date, end_date, label=None):
        """
        List Transactions - Handles special case where "Unclassified" is converted to empty string
        :return: formats results for display or returns transactions list
        """
        if label == "Unclassified":
            label = ""

        transactions = self._transaction_access.get_transactions(start_date, end_date, label)

        if self._report_access:
            return self._report_access.format_transaction_list(transactions)
        return transactions

    def report_expenditures(self, start_date, end_date):
        """
        Report Expenditure - spending by label for the date range
        :return: formats the results for display or returns expenditure dictionary
        """
        expenditures = self._transaction_access.get_transaction_labels(start_date, end_date)

        if "" in expenditures:
            expenditures["Other"] = expenditures[""]
            del expenditures[""]

        if self._report_access:
            return self._report_access.format_expenditure_report(expenditures)
        return expenditures







