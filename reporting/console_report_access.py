from interfaces.report_access import IReportAccess

class ConsoleReportAccess(IReportAccess):
    def format_transaction_list(self, transactions):
        """
        Takes date, description, amount and format into string.
        :returns: list of formated strings
        """
        result = []
        for t in transactions:
            line = f"{t.get_date().isoformat()} {t.get_description()}: {t.get_amount():.2f}"
            # checks if label, true appends [label] false appends empty []
            if t.get_label():
                line += f" [{t.get_label()}]"
            else:
                line += " []"
            result.append(line)
        result.append(f"{len(transactions)} transaction(s) listed")
        return result

    def format_classification_result(self, transactions):
        """
        Formats each transaction with date, description, and amount
        :returns: list with all formatted lines plus summary line
        """
        result = []
        for t in transactions:
            line = f"{t.get_date().isoformat()} {t.get_description()}: {t.get_amount():.2f}"
            # checks label, appends with label, or "unable to classify"
            if t.get_label():
                line += f" classified as {t.get_label()}"
            else:
                line += " unable to classify"
            result.append(line)
        result.append(f"{len(transactions)} transaction(s) processed")
        return result

    def format_expenditure_report(self, expenditures):
        """
        Takes dictionary of labels, calculates total amounts
        :returns: list of formated strings
        """
        result = []
        total = 0
        for label, amount in expenditures.items():
            if label:
                result.append(f"{label}: {amount:.2f}")
            else:
                result.append(f"Other: {amount:.2f}")
            total += amount
        result.append(f"Total: {total:.2f}")
        return result