""" Filter calendar """

import json
import re
import warnings
from collections import namedtuple
from pathlib import Path
from typing import Optional, List, Callable, Union

import arrow
from arrow import Arrow
from ics import Calendar, Event

DATE_FMT = "YYYY-MM-DD"


class CalendarFilter:
    def __init__(
        self,
        input_file: Path,
        re_pattern: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        output_format="json",
    ):
        """Filter calendar and output in either ics or json format

        Arguments:
            input_file {Path} -- filepath to calendar file in ics format

        Keyword Arguments:
            re_pattern {Optional[str]} -- regular expression pattern to 
            filter event.name and event.description (default: {None})
            start_date {Optional[str]} -- start date (inclusive) in YYYY-MM-DD (default: {None})
            end_date {Optional[str]} -- end date (inclusive) in YYYY-MM-DD (default: {None})
            If end_date is None, the current date with `arrow.now()` is set.
            output_format {str} -- output file format either in ics (calendar) format or json (default: {"json"})

        Raises:
            ValueError: if end_date is given but not for the start_date
        """
        self.input_file = input_file
        self.re_pattern = re_pattern
        self.start_date = start_date
        self.end_date = end_date
        self.output_format = output_format

        if self.start_date and (self.end_date is None):
            self.end_date = arrow.now()
            warnings.warn(f"end_date is set to {self.end_date!s}")

        if self.end_date and (self.start_date is None):
            raise ValueError(f"start_date is required")

        if self.start_date and isinstance(self.start_date, str):
            self.start_date = arrow.get(self.start_date, DATE_FMT)
        if self.end_date and isinstance(self.end_date, str):
            self.end_date = arrow.get(self.end_date, DATE_FMT)

        if output_format == "json":
            self.result = []
        if output_format == "ics":
            self.result = Calendar()

    def create_filter_functions(self) -> [Callable]:
        result = []
        if self.re_pattern:
            result.append(self.check_re_pattern)
        if self.start_date and self.end_date:
            result.append(self.check_within_date)
        return result

    def get_calendars(self) -> List[Calendar]:
        with open(self.input_file, "rt") as in_f:
            cal_text = in_f.read()
            cals = Calendar.parse_multiple(cal_text)
        return cals

    def filter_calendars(self):
        filter_functions = self.create_filter_functions()
        cals = self.get_calendars()
        for cal in cals:
            self.filter_events(cal=cal, filter_functions=filter_functions)

    def filter_events(self, cal: Calendar, filter_functions):
        for e in cal.events:
            if all(f(e) for f in filter_functions):
                self.add_result(result=self.result, event=e)
            else:
                continue

    def check_re_pattern(self, event: Event) -> bool:
        if re.search(
            self.re_pattern, fr"{event.name} {event.description}", re.IGNORECASE
        ):
            return True
        return False

    def check_within_date(self, event: Event) -> bool:
        if self.start_date <= event.begin <= self.end_date:
            return True
        return False

    @staticmethod
    def add_result(result: Union[List, Calendar], event: Event):
        if type(result) is Calendar:
            result.events.add(event)
        if type(result) is list:
            result.append(
                {
                    "name": event.name,
                    "start": event.begin.format(DATE_FMT),
                    "duration": event.duration.total_seconds(),
                }
            )

    def save_as(self, output_file):
        with open(output_file, "w") as out_f:
            if isinstance(self.result, Calendar):
                out_f.write(str(self.result))
            if isinstance(self.result, list):
                json.dump(self.result, out_f)

    @classmethod
    def filter(
        cls,
        input_file,
        output_file,
        re_pattern=None,
        start_date=None,
        end_date=None,
        output_format="json",
    ):
        filter_calendar = cls(
            input_file=input_file,
            re_pattern=re_pattern,
            start_date=start_date,
            end_date=end_date,
            output_format=output_format,
        )
        filter_calendar.filter_calendars()
        filter_calendar.save_as(output_file)
