#!/usr/bin/env python

"""Tests for `calh` package."""
from pathlib import Path

import pytest
from click.testing import CliRunner
from ics import Calendar

from calh.filter import CalendarFilter
from . import CURR_DIR

# These are the last 10 events from urlab.ics from 02 April to 05 May
# [<Event 'SmartMonday de Mai 2020' begin:2020-05-04T17:00:12+00:00 end:2020-05-04T19:30:12+00:00>,
#  <Event 'Workshop Make no2' begin:2020-03-12T11:00:39+00:00 end:2020-03-12T13:00:39+00:00>,
#  <Event 'Workshop Make no1' begin:2020-03-10T11:00:40+00:00 end:2020-03-10T13:00:41+00:00>,
#  <Event 'SmartMonday de Mars 2020' begin:2020-03-09T18:00:22+00:00 end:2020-03-09T21:30:22+00:00>,
#  <Event 'Réunion débat timent' begin:2020-02-25T17:30:00+00:00 end:2020-02-25T19:00:00+00:00>,
#  <Event 'Mardi C'est root-me' begin:2020-02-18T18:00:00+00:00 end:2020-02-18T20:00:00+00:00>,
#  <Event 'Workshop réseaux de neurones' begin:2020-02-17T17:30:00+00:00 end:2020-02-17T22:00:00+00:00>,
#  <Event '« Et demain ? »' begin:2020-02-13T15:30:01+00:00 end:2020-02-13T17:30:01+00:00>,
#  <Event 'VenDreDDi' begin:2020-02-07T16:00:10+00:00 end:2020-02-07T21:00:10+00:00>,
#  <Event 'La première réunion du quadri' begin:2020-02-04T18:30:34+00:00 end:2020-02-04T20:00:34+00:00>]


def test_filter_calendar_without_any_filter():
    filtered_calendar = CalendarFilter(
        input_file=Path(CURR_DIR / "data" / "ics" / "02-04_05-05-2020_urlab.ics"),
    )
    filtered_calendar.filter_calendars()
    result = filtered_calendar.result
    expected_result = [
        {"name": "SmartMonday de Mai 2020", "start": "2020-05-04", "duration": 9000.0},
        {"name": "Mardi C'est root-me", "start": "2020-02-18", "duration": 7200.0},
        {"name": "Workshop Make no1", "start": "2020-03-10", "duration": 7201.0},
        {"name": "VenDreDDi", "start": "2020-02-07", "duration": 18000.0},
        {
            "name": "La première réunion du quadri",
            "start": "2020-02-04",
            "duration": 5400.0,
        },
        {"name": "Réunion débat timent", "start": "2020-02-25", "duration": 5400.0},
        {
            "name": "SmartMonday de Mars 2020",
            "start": "2020-03-09",
            "duration": 12600.0,
        },
        {"name": "Workshop Make no2", "start": "2020-03-12", "duration": 7200.0},
        {
            "name": "Workshop réseaux de neurones",
            "start": "2020-02-17",
            "duration": 16200.0,
        },
        {"name": "« Et demain ? »", "start": "2020-02-13", "duration": 7200.0},
    ]
    assert result == expected_result


def test_filter_cals_by_date():
    filtered_calendar = CalendarFilter(
        input_file=Path(CURR_DIR / "data" / "ics" / "02-04_05-05-2020_urlab.ics"),
        start_date="2020-02-04",
        end_date="2020-05-05",
    )
    filtered_calendar.filter_calendars()
    result = filtered_calendar.result
    expected_result = [
        {"name": "SmartMonday de Mai 2020", "start": "2020-05-04", "duration": 9000.0},
        {"name": "Mardi C'est root-me", "start": "2020-02-18", "duration": 7200.0},
        {"name": "Workshop Make no1", "start": "2020-03-10", "duration": 7201.0},
        {"name": "VenDreDDi", "start": "2020-02-07", "duration": 18000.0},
        {
            "name": "La première réunion du quadri",
            "start": "2020-02-04",
            "duration": 5400.0,
        },
        {"name": "Réunion débat timent", "start": "2020-02-25", "duration": 5400.0},
        {
            "name": "SmartMonday de Mars 2020",
            "start": "2020-03-09",
            "duration": 12600.0,
        },
        {"name": "Workshop Make no2", "start": "2020-03-12", "duration": 7200.0},
        {
            "name": "Workshop réseaux de neurones",
            "start": "2020-02-17",
            "duration": 16200.0,
        },
        {"name": "« Et demain ? »", "start": "2020-02-13", "duration": 7200.0},
    ]
    assert result == expected_result


def test_filter_calendar_by_re_pattern():
    filtered_calendar = CalendarFilter(
        input_file=Path(CURR_DIR / "data" / "ics" / "02-04_05-05-2020_urlab.ics"),
        re_pattern="workshop",
    )
    filtered_calendar.filter_calendars()
    result = filtered_calendar.result
    expected_result = [
        {"name": "Workshop Make no1", "start": "2020-03-10", "duration": 7201.0},
        {"name": "Workshop Make no2", "start": "2020-03-12", "duration": 7200.0},
        {
            "name": "Workshop réseaux de neurones",
            "start": "2020-02-17",
            "duration": 16200.0,
        },
    ]
    assert result == expected_result


def test_filter_calendar_by_date_and_re_pattern():
    filtered_calendar = CalendarFilter(
        input_file=Path(CURR_DIR / "data" / "ics" / "urlab.ics"),
        re_pattern="workshop",
        start_date="2020-02-04",
        end_date="2020-05-04",
    )
    filtered_calendar.filter_calendars()
    result = filtered_calendar.result
    assert result == [
        {
            "name": "Workshop réseaux de neurones",
            "start": "2020-02-17",
            "duration": 16200.0,
        },
        {"name": "Workshop Make no2", "start": "2020-03-12", "duration": 7200.0},
        {"name": "Workshop Make no1", "start": "2020-03-10", "duration": 7201.0},
    ]


def test_filter_calendar_to_output_ics():
    filtered_calendar = CalendarFilter(
        input_file=CURR_DIR / "data" / "ics" / "urlab.ics",
        start_date="2020-02-04",
        end_date="2020-05-05",
        output_format="ics",
    )
    filtered_calendar.filter_calendars()
    result = filtered_calendar.result
    assert isinstance(result, Calendar)
    with open(Path(CURR_DIR / "data" / "ics" / "02-04_05-05-2020_urlab.ics")) as in_f:
        expected_cal = Calendar(in_f.read())
    assert result.events == expected_cal.events
