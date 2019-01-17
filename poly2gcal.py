#!/usr/bin/python3

## poly2gcal - add PolyMTL classes to Google Calendar
## author: Christophe Bedard

import argparse
import json
from datetime import datetime, timedelta
from oauth2client.client import AccessTokenRefreshError

from gcal import login, create_calendar_body, create_event_body
from time_tools import date_to_datetime
from conversion_tools import convert_semester_info, convert_courses
from weekdates_intervals import get_interval

# parse
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('-t',
                    dest='test',
                    action='store_const',
                    const=True,
                    default=False,
                    help='test: only preview requests & do not actually add to calendar')
parser.add_argument('-c',
                    dest='checklist',
                    action='store_const',
                    const=True,
                    default=False,
                    help='generate checklist of labs to hand in, separated by weeks')
args = parser.parse_args()
test = args.test
checklist = args.checklist

def is_in_semester(date_time, semester_info):
    """
    Check if a datetime is within the first and last days of the semester
    """
    return semester_info['first_day'] <= date_time.date() <= semester_info['last_day']

def is_holiday(date, semester_info):
    """
    Check if a date is a holiday
    """
    return date.date() in semester_info['holidays']

def is_alt_week_exception(date_time, semester_info):
    """
    Check if a datetime corresponds to an exception to the usual week alternation rule
    (i.e. Monday might be B1 while the rest of the week is B2)
    """
    return date_time.date() in semester_info['alt_exceptions']

def insert_event(service, course_name, calendar_ids, body):
    """
    Insert an event (but only if the test flag is not enabled)
    """
    print('EVENT:\n' + repr(body))
    if not test:
        response_event = service.events().insert(calendarId=calendar_ids[course_name], body=body).execute()

def insert_calendar(service, body, course_name, calendar_ids):
    """
    Insert a calendar (but only if the test flag is not enabled)
    """
    print('CALENDAR:\n' + repr(body))
    if not test:
        response_cal = service.calendars().insert(body=body).execute()
        calendar_ids[course_name] = response_cal['id']

def check_lab(week_day, week_alt_lab, course_name, lab, service, semester_info, calendar_ids):
    """
    Check if there is a lab in a given week and insert if there is
    """
    start = date_to_datetime(week_day) + lab['start']
    if is_in_semester(start, semester_info) and not is_holiday(start, semester_info):
        lab_alt_week = lab['week']
        current_week_alt = week_alt_lab
        # if this day is an exception, flip the current week
        if lab_alt_week and is_alt_week_exception(start, semester_info):
            current_week_alt = flip_alt_week(current_week_alt)
        # if the lab is weekly anyway or if this is the corresponding alt week
        if not lab_alt_week or lab_alt_week == current_week_alt:
            if not checklist:
                end = start + lab['duration']
                event_name = 'Lab - ' + course_name
                event = create_event_body(event_name, lab['room'], start, end)
                insert_event(service, course_name, calendar_ids, event)
            else:
                print('Lab {} done'.format(course_name))

def insert_lectures(week_day, course_name, lectures, service, semester_info, calendar_ids):
    """
    Insert lectures for a course for a given week
    """
    for lecture in lectures:
        start = date_to_datetime(week_day) + lecture['start']
        if is_in_semester(start, semester_info) and not is_holiday(start, semester_info):
            end = start + lecture['duration']
            event_name = 'Cours - ' + course_name
            event = create_event_body(event_name, lecture['room'], start, end)
            insert_event(service, course_name, calendar_ids, event)

def process_week(week_day, week_alt_lab, service, semester_info, courses, calendar_ids):
    """
    Process all courses (lectures and labs) for a given week
    """
    for course in courses:
        course_name = course['name']
        check_lab(week_day, week_alt_lab, course_name, course['lab'], service, semester_info, calendar_ids)
        if not checklist:
            insert_lectures(week_day, course_name, course['lectures'], service, semester_info, calendar_ids)

def flip_alt_week(alt_week):
    """
    Flip an alternate week value
    """
    return 'B2' if alt_week == 'B1' else 'B1'

def process_semester(service, semester_info, courses, calendar_ids):
    """
    Process the whole semester, adding lectures and labs
    """
    # week by week
    week_day = semester_info['firstweek_day']
    week_alt_lab = 'B1'
    while week_day <= semester_info['lastweek_day']:
        if checklist:
            print(get_interval(week_day))
        if week_day != semester_info['breakweek_day']:
            process_week(week_day, week_alt_lab, service, semester_info, courses, calendar_ids)
            week_alt_lab = flip_alt_week(week_alt_lab)
        week_day += timedelta(weeks=1)

def create_calendars(service, courses):
    """
    Create a calendar for each course
    """
    calendar_ids = {}
    for course in courses:
        course_name = course['name']
        calendar = create_calendar_body(course_name)
        insert_calendar(service, calendar, course_name, calendar_ids)
    return calendar_ids

def main():
    """
    Main logic: get API service and process input data
    """
    service = login() if not test else None

    with open('input_data.json') as f:
        data = json.load(f)

    semester_info = data['semester_info']
    convert_semester_info(semester_info)
    courses = convert_courses(data['courses'])

    try:
        calendar_ids = create_calendars(service, courses) if not checklist else None
        process_semester(service, semester_info, courses, calendar_ids)
    
    except AccessTokenRefreshError:
        print('The credentials have been revoked or expired, please re-run the application to re-authorize')

if __name__ == '__main__':
    main()
