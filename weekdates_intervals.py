#!/usr/bin/python3

## Generate week intervals
# Used for grouping checklist items
# example: "Week of January 7 to 13:"

import json
from datetime import datetime, timedelta
from time_tools import month_from_datetime
from conversion_tools import convert_semester_info, convert_courses


def main():
    with open('input_data.json') as f:
        data = json.load(f)

    semester_info = data['semester_info']
    convert_semester_info(semester_info)

    first_day = semester_info['firstweek_day']
    while first_day <= semester_info['lastweek_day']:
        last_day = first_day + timedelta(days=6)
        
        begin_month = month_from_datetime(first_day)
        end_month = month_from_datetime(last_day)

        print('Week of {} {} to{} {}:'.format(begin_month,
                                              str(first_day.day),
                                              ' {}'.format(end_month) if begin_month != end_month else '',
                                              str(last_day.day)))

        first_day += timedelta(weeks=1)

if __name__ == '__main__':
    main()
