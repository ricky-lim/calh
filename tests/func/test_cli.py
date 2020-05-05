import json
from pathlib import Path

from click.testing import CliRunner

from calh.cli import cli

CURR_DIR = Path(__file__).parent


def test_filter_calendar():
    runner = CliRunner()
    input_file = f'{Path(CURR_DIR / "data" / "ics"/ "urlab.ics")}'
    output_file = f'{Path(CURR_DIR / "data" / "json"/"filtered_urlab.json")}'
    result = runner.invoke(
        cli,
        [
            "filter-calendar",
            "--input-file",
            input_file,
            "--re-pattern",
            "workshop",
            "--start-date",
            "2020-02-04",
            "--end-date",
            "2020-05-05",
            "--output-file",
            output_file,
        ],
    )
    assert result.exit_code == 0
    assert Path(output_file).exists()
    Path(output_file).unlink()


def draw_calendar(input_file, output_file, full_year=False):
    runner = CliRunner()
    cmd = [
        "draw-calendar",
        "--input-file",
        input_file,
        "--title",
        "Test",
        "--output-file",
        output_file,
    ]
    if full_year:
        cmd.append("--full-year")
    result = runner.invoke(cli, cmd)
    return result


def test_draw_calendar():
    input_file = f'{Path(CURR_DIR / "data" / "json" / "02-04_05-05-2020_urlab.json")}'
    output_file = f'{Path(CURR_DIR / "data" / "png" /"filtered_urlab.png")}'
    result = draw_calendar(input_file=input_file, output_file=output_file)
    assert result.exit_code == 0
    assert Path(output_file).exists()
    Path(output_file).unlink()


def test_draw_calendar_with_full_year():
    input_file = f'{Path(CURR_DIR / "data" / "json" / "02-04_05-05-2020_urlab.json")}'
    output_file = (
        f'{Path(CURR_DIR / "data" / "png" / "filtered_urlab-with-full-year.png")}'
    )
    result = draw_calendar(
        input_file=input_file, output_file=output_file, full_year=True
    )
    assert result.exit_code == 0
    assert Path(output_file).exists()
    Path(output_file).unlink()
