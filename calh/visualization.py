import calendar
import datetime
import json
import math
from datetime import timedelta
from pathlib import Path
from typing import Union, Dict, List

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from ics import Calendar

from calh.filter import CalendarFilter


class Heatmap:
    def __init__(self, input_data: Union[Path, List], full_year=True):
        """Generate heatmap

        Arguments:
            input_data {Union[Path, List]} -- Input data can be a filepath (Path) or a python list object

        Keyword Arguments:
            full_year {bool} -- Show the whole year, if True.
            Otherwise it will show only months where events are found (default: {True})

        Raises:
            ValueError: if the file_path contains no data
        """

        self.input_data = input_data
        self.full_year = full_year
        data = self.read_input_data(input_data)
        self.df = self.create_df(data)
        self.result = None

    def read_input_data(self, input_data):
        """Reading input data

        Arguments:
            input_data {Union[Path, List]} -- Input data can be a filepath (Path) or a python list object

        Raises:
            ValueError: if Object is not a list
            ValueError: if data is empty
        """
        input_reader = {
            ".ics": self.read_ics,
            ".json": self.read_json,
        }
        try:
            reader = input_reader[Path(input_data).suffix]
            data = reader(input_data)
        except TypeError:
            if isinstance(self.input_data, list):
                # This is a shallow-copy to keep data immutable!
                data = input_data.copy()
            else:
                raise ValueError("Unknown input")
        if not data:
            raise ValueError("No data")
        return data

    @staticmethod
    def read_ics(file_path: Path) -> List[Dict]:
        with open(file_path, "rt") as in_f:
            cals = Calendar.parse_multiple(in_f.read())
        result = []
        for c in cals:
            for e in c.events:
                CalendarFilter.add_result(result=result, event=e)
        return result

    @staticmethod
    def read_json(file_path: Path) -> List[Dict]:
        with open(file_path, "r") as in_f:
            result = json.load(in_f)
        return result

    @staticmethod
    def create_df(data):
        df = pd.DataFrame(data)
        df["start"] = pd.to_datetime(df["start"])
        df["date"] = df["start"].dt.floor("d")
        return df

    def create_date_df(self, df):
        by_date = df.groupby("date")[["name"]].count()
        by_date = by_date.sort_index()
        by_date["weekday"] = by_date.index.weekday
        by_date["date"] = by_date.index
        by_date["week"] = by_date.date.apply(lambda x: int(x.isocalendar()[1]))
        by_date["month"] = by_date.index.month
        return by_date

    def get_activities(
        self, date_df: pd.DataFrame, min_week: int, max_week: int
    ) -> np.ndarray:
        """Create a matrix of weekday and isoweek

        Arguments:
            date_df {pd.DataFrame} -- dataframe containing date properties
            min_week {int} -- smallest week number
            max_week {int} -- largest week number

        Returns:
            np.ndarray -- a matrix of weekday (y) and isoweek (x)
        """
        activities = np.full((7, (max_week - min_week) + 1), np.nan)
        for idx, row in date_df.iterrows():
            normalized_week = row["week"] - min_week
            activities[row["weekday"]][normalized_week] = row["name"]
        return activities

    @staticmethod
    def isomonth_number_for(year: int, week: int) -> int:
        first = datetime.date(year, 1, 1)
        base = 1 if first.isocalendar()[1] == 1 else 8
        date = first + timedelta(days=base - first.isocalendar()[2] + 7 * (week - 1))
        return date.month

    def create_labels(
        self, min_week: int, max_week: int, year: int,
    ):
        """Create x_label and y_label for a heatmap.

        Arguments:
            min_week {int} -- smallest number of week
            max_week {int} -- largest number of week
            year {int} -- year of calendar

        Returns:
            tuple -- a tuple containing a list of `x_labels` and a list of `y_label`
        """
        month_nums = [
            self.isomonth_number_for(year=year, week=wk + 1)
            for wk in range(min_week, max_week)
        ]
        x_labels = [calendar.month_abbr[month_nums[0]]]
        for i in range(1, len(month_nums) - 1):
            if month_nums[i - 1] != month_nums[i]:
                month = calendar.month_abbr[month_nums[i]]
                x_labels.append(month)
            else:
                x_labels.append("")

        y_labels = ["Mon", "", "Wed", "", "Fri", "", "Sun"]
        return (x_labels, y_labels)

    @staticmethod
    def get_unique_years(df) -> List[int]:
        return list(pd.DatetimeIndex(df["date"]).year.unique())

    def draw(self, title, width=None, height=None):
        years = sorted(self.get_unique_years(self.df), reverse=True)
        num_year = len(years)
        if width is None:
            width = 20
        if height is None:
            height = 5 * num_year // 2
        fig, axs = plt.subplots(num_year, figsize=(width, height), squeeze=False)
        fig.patch.set_facecolor("white")
        fig.tight_layout(pad=3.0)
        for idx, year in enumerate(years):
            yearly_df = self.df[self.df["date"].dt.year == year]
            ax = axs[idx, 0]
            self.draw_yearly(yearly_df=yearly_df, ax=ax, year=year)
        fig.suptitle(title.title(), fontsize=20, verticalalignment="top", y=1.1)
        self.result = fig

    @staticmethod
    def isoweek_number_for(year: int):
        last_week = datetime.date(year, 12, 28)
        return last_week.isocalendar()[1]

    def draw_yearly(self, yearly_df, ax, year):
        date_df = self.create_date_df(yearly_df)
        if self.full_year:
            min_week = 1
            max_week = self.isoweek_number_for(year)
        else:
            min_week = date_df.week.min()
            max_week = date_df.week.max()
        activities = self.get_activities(
            date_df=date_df, min_week=min_week, max_week=max_week
        )
        x_labels, y_labels = self.create_labels(
            min_week=min_week, max_week=max_week, year=year,
        )
        ax.set_title(year, fontsize=10, loc="left")
        ax.xaxis.tick_top()
        ax.tick_params(axis="both", which="both", length=0)
        ax.set_facecolor("#ebedf0")

        sns.heatmap(
            activities,
            linewidths=2,
            linecolor="white",
            square=True,
            mask=np.isnan(activities),
            cmap="Greens",
            vmin=0,
            vmax=100,
            cbar=False,
            ax=ax,
        )

        ax.set_yticklabels(y_labels, rotation=0)
        ax.set_xticklabels(x_labels, ha="left")

    def save_as(self, output_file, *args, **kwargs):
        self.result.savefig(output_file, bbox_inches="tight", *args, **kwargs)

    @classmethod
    def create(
        cls, input_file, output_file, title, full_year=True, width=None, height=None
    ):
        hm = Heatmap(input_data=input_file, full_year=full_year)
        hm.draw(title=title, width=width, height=height)
        hm.save_as(output_file=output_file)
