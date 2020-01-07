"""
Module to generate week intervals.

Used for grouping items.
example: 'Week of January 7 to 13:'
"""

from datetime import datetime
from datetime import timedelta
import json

from .conversion_tools import convert_courses
from .conversion_tools import convert_semester_info
from .time_tools import month_from_date


def get_interval(
    start: datetime,
) -> str:
    """
    Format an interval (starting at the begin date) to string

    :param begin: the start date
    """
    end = start + timedelta(days=6)
    start_month = month_from_date(start)
    end_month = month_from_date(end)
    return (
        f'Week of {start_month} {start.day} '
        f'to{" " + end_month if start_month != end_month else ""} {end.day}:'
    )


def print_intervals(
    data_file: str = 'input_data.json',
) -> None:
    with open(data_file) as f:
        data = json.load(f)

    semester_info = data['semester_info']
    convert_semester_info(semester_info)

    first_day = semester_info['firstweek_day']
    while first_day <= semester_info['lastweek_day']:
        print(get_interval(first_day))
        first_day += timedelta(weeks=1)
