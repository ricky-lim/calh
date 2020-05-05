import arrow
import pytest
from calh.filter import CalendarFilter


def test_calendar_filter_with_no_end_date():
    date_format = "%Y-%m-%d"
    cal = CalendarFilter(input_file="foo", start_date="2020-01-01", end_date=None)
    expected_end_date = arrow.now().strftime(date_format)
    assert cal.end_date.strftime(date_format) == expected_end_date


def test_calendar_filter_with_no_start_date():
    with pytest.raises(ValueError) as e:
        cal = CalendarFilter(input_file="foo", start_date=None, end_date="2020-01-01")
    assert 'start_date is required' in str(e)
