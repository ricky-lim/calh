import sys
from pathlib import Path

import click
from ics import Calendar

from calh.filter import CalendarFilter


@click.group()
def cli():
    pass


def create_single_year_dataset():
    input_file = Path(__file__).parent / "func" / "data" / "urlab.ics"
    output_file = Path(__file__).parent / "func" / "data" / "02-04_05-05-2020_urlab.ics"
    CalendarFilter.filter(
        input_file=input_file,
        start_date="2020-02-04",
        end_date="2020-05-05",
        output_format="ics",
        output_file=output_file,
    )


def create_multiple_year_dataset():
    input_file = Path(__file__).parent / "func" / "data" / "urlab.ics"
    output_file = Path(__file__).parent / "func" / "data" / "2018-2020_urlab.ics"
    cal_filter = CalendarFilter.filter(
        input_file=input_file,
        start_date="2018-01-01",
        end_date="2020-01-01",
        output_format="ics",
        output_file=output_file,
    )


@cli.command()
def create_test_data():
    create_single_year_dataset()
    create_multiple_year_dataset()


if __name__ == "__main__":
    sys.exit(cli())
