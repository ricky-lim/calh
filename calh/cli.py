"""Console script for calh."""
import json
import sys

import click
import click_spinner


@click.group(invoke_without_command=True)
@click.option("-v", "--version", is_flag=True, default=False)
def cli(version):
    if version:
        import calh

        click.echo(f"Version: {calh.__version__}")


@cli.command()
@click.option(
    "--input-file", required=True, type=click.Path(), help="Calendar filepath"
)
@click.option("--re-pattern", default=None, help="Regular expression pattern")
@click.option(
    "--start-date", default=None, help="Date starts from. Format in YYYY-MM-DD"
)
@click.option("--end-date", default=None, help="Date untill. Format in YYYY-MM-DD")
@click.option(
    "--output-format",
    type=click.Choice(["json", "ics"]),
    default="json",
    help="Output format",
)
@click.option("--output-file", type=click.Path(), help="Filepath for your output")
def filter_calendar(
    input_file, re_pattern, start_date, end_date, output_format, output_file
):
    """
    Filter ics-format calendar
    """
    from calh.filter import CalendarFilter

    with click_spinner.spinner():
        CalendarFilter.filter(
            input_file=input_file,
            re_pattern=re_pattern,
            start_date=start_date,
            end_date=end_date,
            output_format=output_format,
            output_file=output_file,
        )

    click.echo(f"Your filtered calendar is ready: {output_file}")


@cli.command()
@click.option("--input-file", required=True, type=click.Path(), help="Input file")
@click.option("--title", required=True, help="Title of the calendar")
@click.option("--width", default=None, help="Width in inch")
@click.option("--height", default=None, help="Height in inch")
@click.option("--full-year", is_flag=True, default=False, help="Show the full year")
@click.option("--output-file", type=click.Path(), help="out json file")
def draw_calendar(input_file, title, full_year, width, height, output_file):
    """
    Drawing calender with weekdays and iso-weeks
    """
    from calh.visualization import Heatmap

    with click_spinner.spinner():
        Heatmap.create(
            input_file=input_file,
            full_year=full_year,
            output_file=output_file,
            title=title,
            width=width,
            height=height,
        )

    click.echo(f"Your calendar is ready: {output_file}")


if __name__ == "__main__":
    sys.exit(cli())  # pragma: no cover
