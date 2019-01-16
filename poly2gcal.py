#!/usr/bin/python3

## poly2gcal - add PolyMTL classes to Google Calendar
## author: Christophe Bedard

import argparse
import json
from datetime import datetime, timedelta
from oauth2client.client import AccessTokenRefreshError

from gcal import login, create_calendar_body, create_event_body
from conversion_tools import convert_semester_info, convert_courses

# parse
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('-t',
                    dest='test',
                    action='store_const',
                    const=True,
                    default=False,
                    help='test: only preview requests & do not actually add to calendar')
args = parser.parse_args()
test = args.test


def insert_lectures(week_day, course, service, semester_info, calendar_ids):
    course_name = course['name']
    for lecture in course['lectures']:
        start = week_day + lecture['start']
        is_holiday = start.date() in semester_info['holidays']
        is_in_semester = semester_info['first_day'].date() <= start.date() <= semester_info['last_day'].date()
        if is_in_semester and not is_holiday:
            end = start + lecture['duration']
            event_name = 'Cours - ' + course_name
            event = create_event_body(event_name, lecture['room'], start, end)
            print('INSERT:\n' + repr(event))
            if not test:
                response_event = service.events().insert(calendarId=calendar_ids[course_name], body=event).execute()

def process_week(week_day, service, semester_info, courses, calendar_ids):
    for course in courses:
        insert_lectures(week_day, course, service, semester_info, calendar_ids)

def process_semester(service, semester_info, courses, calendar_ids):
    # week by week
    week_day = semester_info['firstweek_day']
    while week_day <= semester_info['lastweek_day']:
        if week_day != semester_info['breakweek_day']:
            process_week(week_day, service, semester_info, courses, calendar_ids)
        week_day += timedelta(weeks=1)

def create_calendars(service, courses):
    calendar_ids = {}
    for course in courses:
        course_name = course['name']
        calendar = create_calendar_body(course_name)
        print('CREATE:\n' + repr(calendar))
        if not test:
            response_cal = service.calendars().insert(body=calendar).execute()
            calendar_ids[course_name] = response_cal['id']
    return calendar_ids

def main():
    service = login() if not test else None

    with open('input_data.json') as f:
        data = json.load(f)

    semester_info = data['semester_info']
    convert_semester_info(semester_info)
    courses = convert_courses(data['courses'])

    try:
        calendar_ids = create_calendars(service, courses)
        process_semester(service, semester_info, courses, calendar_ids)
    
    except AccessTokenRefreshError:
        print('The credentials have been revoked or expired, please re-run the application to re-authorize')

if __name__ == '__main__':
    main()
