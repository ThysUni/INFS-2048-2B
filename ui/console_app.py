import click
from datetime import date
from storage.file_based_storage import FileBasedStorage
from classification.csv_rule_access import CSVRuleAccess
from classification.classification_engine import ClassificationEngine
from reporting.console_report_access import ConsoleReportAccess
from reporting.reporting_manager import ReportingManager


class ConsoleApp:
    def __init__(self):
        rule_access = CSVRuleAccess()
        classification_engine = ClassificationEngine(rule_access)
        self.reporting_manager = ReportingManager(FileBasedStorage(), classification_engine)
        self.reporting_manager.set_report_access(ConsoleReportAccess())

    def run_cli(self):
        cli()

    def parse_args(self, args):
        cli(args)


@click.group()
def cli():
    pass


@cli.command("import")
@click.argument('filepath')
def import_cmd(filepath):
    count = app.reporting_manager.import_transactions(filepath)
    click.echo(f"Imported {count} transactions.")


@cli.command()
@click.argument('start_date')
@click.argument('end_date')
@click.option('--rules', default='patterns.csv', help='Path to rules file')
def classify(rules, start_date, end_date):
    start = date.fromisoformat(start_date)
    end = date.fromisoformat(end_date)
    results = app.reporting_manager.classify_transactions(rules, start, end)
    for line in results:
        click.echo(line)


@cli.command()
@click.argument('start_date')
@click.argument('end_date')
@click.option('--label', default=None, help='Filter by label')
def list(start_date, end_date, label):
    start = date.fromisoformat(start_date)
    end = date.fromisoformat(end_date)
    results = app.reporting_manager.list_transactions(start, end, label)
    for line in results:
        click.echo(line)


@cli.command()
@click.argument('start_date')
@click.argument('end_date')
def report(start_date, end_date):
    start = date.fromisoformat(start_date)
    end = date.fromisoformat(end_date)
    results = app.reporting_manager.report_expenditures(start, end)
    for line in results:
        click.echo(line)


# Create the application instance
app = ConsoleApp()