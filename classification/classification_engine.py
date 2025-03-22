from interfaces.rule_access import IRuleAccess

class ClassificationEngine:
    def __init__(self, rule_access):
        self._rule_access = rule_access

    def apply_classification_rules(self, transactions, rules_path):
        self._rule_access.load_rules(rules_path)
        classified_transactions = []

        for transaction in transactions:
            description = transaction.get_description().lower()

            for pattern in self._rule_access._rules_cache:
                if pattern.lower() in description:
                    label = self._rule_access._rules_cache[pattern]
                    transaction.set_label(label)
                    break # first match wins

            classified_transactions.append(transaction)

        return classified_transactions




        