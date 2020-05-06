import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from calh.visualization import Heatmap
from . import CURR_DIR


def test_date_df_for_heatmap_from_ics_input():
    hm = Heatmap(input_data=CURR_DIR / "data" / "ics" / "02-04_05-05-2020_urlab.ics")
    expected_date_df = pd.DataFrame(
        [
            {"name": 1, "weekday": 1, "date": "2020-02-04", "week": 6, "month": 2},
            {"name": 1, "weekday": 4, "date": "2020-02-07", "week": 6, "month": 2},
            {"name": 1, "weekday": 3, "date": "2020-02-13", "week": 7, "month": 2},
            {"name": 1, "weekday": 0, "date": "2020-02-17", "week": 8, "month": 2},
            {"name": 1, "weekday": 1, "date": "2020-02-18", "week": 8, "month": 2},
            {"name": 1, "weekday": 1, "date": "2020-02-25", "week": 9, "month": 2},
            {"name": 1, "weekday": 0, "date": "2020-03-09", "week": 11, "month": 3},
            {"name": 1, "weekday": 1, "date": "2020-03-10", "week": 11, "month": 3},
            {"name": 1, "weekday": 3, "date": "2020-03-12", "week": 11, "month": 3},
            {"name": 1, "weekday": 0, "date": "2020-05-04", "week": 19, "month": 5},
        ]
    )
    expected_date_df["date"] = pd.to_datetime(expected_date_df["date"], utc=True)
    date_df = hm.create_date_df(hm.df)
    assert_frame_equal(
        date_df.reset_index(drop=True),
        expected_date_df.reset_index(drop=True),
        check_dtype=False,
        check_index_type=False,
    )


@pytest.mark.mpl_image_compare(
    savefig_kwargs={"bbox_inches": "tight"},
    baseline_dir=str(CURR_DIR / "data" / "png"),
    filename="test_create_heatmap_from_ics_input.png",
)
def test_create_heatmap_from_ics_input():
    input_file = CURR_DIR / "data" / "ics" / "02-04_05-05-2020_urlab.ics"
    output_file = CURR_DIR / "data" / "png" / "02-04_05-05-2020_urlab.png"
    hm = Heatmap(input_data=input_file, full_year=True)
    hm.draw(title="test")
    return hm.result
