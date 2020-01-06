#!/usr/bin/python3

## Generate week intervals
# Used for grouping checklist items
# example: "Week of January 7 to 13:"

import json
from datetime import datetime, timedelta
from time_tools import month_from_date
from conversion_tools import convert_semester_info, convert_courses

def get_interval(date_begin):
    """
    Format an interval (starting at the begin date) to string 
    """
    date_end = date_begin + timedelta(days=6)
    begin_month = month_from_date(date_begin)
    end_month = month_from_date(date_end)
    return 'Week of {} {} to{} {}:'.format(begin_month,
                                           date_begin.day,
                                           ' ' + end_month if begin_month != end_month else '',
                                           date_end.day)

def main():
    with open('input_data.json') as f:
        data = json.load(f)

    semester_info = data['semester_info']
    convert_semester_info(semester_info)

    first_day = semester_info['firstweek_day']
    while first_day <= semester_info['lastweek_day']:
        print(get_interval(first_day))
        first_day += timedelta(weeks=1)

if __name__ == '__main__':
    main()
