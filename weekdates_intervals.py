#!/usr/bin/python3

## Generate week intervals
# Used for grouping checklist items
# example: "Week of January 7 to 13:"

from datetime import datetime, timedelta

# Constants
TIME_FORMAT = '%d/%b/%Y'
MONTH_FORMAT = '%B'
DT_WEEK = timedelta(weeks=1)
DT_WEEK_EXCLUSIVE = timedelta(days=6)

# Parameters
# Note: assuming that a week starts on a Monday
# first day of the first week
firstweek_day = datetime.strptime('7/Jan/2019', TIME_FORMAT)
# first day of the last week
lastweek_day = datetime.strptime('29/Apr/2019', TIME_FORMAT)
# actual last day of the last week
last_day = datetime.strptime('4/May/2019', TIME_FORMAT)

i = firstweek_day
while i <= lastweek_day:
    # If last week, force last day
    if (i == lastweek_day):
        i_end = last_day
    else:
        i_end = i + DT_WEEK_EXCLUSIVE
    
    begin_day = str(i.day)
    begin_month = i.strftime(MONTH_FORMAT)
    end_day = str(i_end.day)
    end_month = i_end.strftime(MONTH_FORMAT)

    # Check if months are the same or not
    if (begin_month == end_month):
        print('Week of ' + begin_month + ' ' + begin_day + ' to ' + end_day + ':')
    else:
        print('Week of ' + begin_month + ' ' + begin_day + ' to ' + end_month + ' ' + end_day + ':')

    i = i + DT_WEEK
