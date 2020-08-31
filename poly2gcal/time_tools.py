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

"""Module for time conversion/processing tools."""

from datetime import date
from datetime import datetime
from datetime import time
from datetime import timedelta


WEEKDAYS_INT = {
    day: i for i, day in enumerate(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])
}


def to_date(
    time_str: str,
) -> date:
    """Get date object from date string."""
    return datetime.strptime(time_str, '%d/%b/%Y').date()


def date_to_datetime(
    date: date,
) -> datetime:
    """Get date object from datetime object."""
    return datetime.combine(date, time())


def weekday_int(
    weekday_str: str,
) -> int:
    """Get the integer corresponding to a day of the week as a string."""
    return WEEKDAYS_INT[weekday_str]


def timedelta_from_day_and_time(
    day: str,
    start: str,
) -> timedelta:
    """Get a timedelta object from a week day (e.g. 'Monday') and a start time (e.g. '0830')."""
    start_time = datetime.strptime(start, '%H%M')
    return timedelta(
        days=weekday_int(day),
        hours=start_time.hour,
        minutes=start_time.minute,
    )


def timedelta_from_class_duration(
    duration: int,
) -> timedelta:
    """Get timedelta from class duration in number of periods/time slots."""
    total_minutes = (60 * duration) - 10
    hours = total_minutes // 60
    minutes = total_minutes % 60
    return timedelta(
        hours=hours,
        minutes=minutes,
    )


def month_from_date(
    date: date,
) -> str:
    """Get month as string from date object."""
    return date.strftime('%B')
