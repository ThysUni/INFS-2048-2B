import csv
from interfaces.rule_access import IRuleAccess

class CSVRuleAccess(IRuleAccess):
    def __init__(self):
        self._rules_cache = {}

    def load_rules(self, filepath):
        self._rules_cache = {} # reset cache
        with open(filepath, 'r') as file:
            reader = csv.reader(file)
            next(reader) # skip header row
            for row in reader:
                if len(row) >= 2:
                    pattern_string, label = row[0], row[1]
                    # Split the pattern string by '|' and create an entry for each individual pattern
                    individual_patterns = pattern_string.split('|')
                    for pattern in individual_patterns:
                        self._rules_cache[pattern] = label
        return len(self._rules_cache)

    def get_rule(self, pattern):
        return self._rules_cache.get(pattern)

test_rule = CSVRuleAccess()
test_rule.load_rules("../examples/patterns.csv")
print(test_rule.get_rule("water"))
print(test_rule.load_rules("../examples/patterns.csv"))




