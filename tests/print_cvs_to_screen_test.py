import csv

def print_csv_contents(csvfile):

    with open(csvfile, 'r', newline='', encoding='utf-8-sig') as csvfile:
        csv_reader = csv.reader(csvfile)

        header = next(csv_reader)
        print(f"Headers: {', '.join(header)}")
        # print(header)
        print("-" * 50)

        for row_number, row in enumerate(csv_reader, 1):
            print(f"Row {row_number}: {', '.join(row)}")

print()
print_csv_contents("../examples/patterns.csv")
print('\n' + '-' * 50)
print_csv_contents("../examples/transactions.csv")
