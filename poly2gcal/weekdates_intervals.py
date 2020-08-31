# Copyright (c) 2019-2020 Christophe Bedard
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
Module to generate week intervals.

Used for grouping items.
example: 'Week of January 7 to 13:'
"""

import json
from datetime import date
from datetime import timedelta

from .conversion_tools import convert_semester_info
from .time_tools import month_from_date


def get_interval(
    start: date,
) -> str:
    """
    Format an interval (starting at the begin date) to string.

    :param begin: the start date
    :return: the interval as a string
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
    """Entrypoint for reading input data file and printing intervals."""
    with open(data_file) as f:
        data = json.load(f)

    semester_info = data['semester_info']
    convert_semester_info(semester_info)

    first_day = semester_info['firstweek_day']
    while first_day <= semester_info['lastweek_day']:
        print(get_interval(first_day))
        first_day += timedelta(weeks=1)
