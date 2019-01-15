#!/usr/bin/python3

## poly2gcal - add classes to calendar

from datetime import datetime, timedelta
from oauth2client.client import AccessTokenRefreshError

from gcal import login, create_calendar_body, create_event_body
from data import *


# get these from the Google API Console: https://console.developers.google.com/
client_id = ''
client_secret = ''


def insert_lectures(week_day, course, service, semester_info, calendar_ids):
    for lecture in course.lectures:
        start = week_day + lecture.start
        if start.date() not in semester_info.holidays:
            end = start + lecture.duration
            event_name = 'Cours - ' + course.name
            event = create_event_body(event_name, lecture.room, start, end)
            # response_event = service.events().insert(calendarId=calendar_ids[course.name], body=event).execute()
            print('INSERT:\n' + repr(event))

def process_week(week_day, service, semester_info, courses, calendar_ids):
    for course in courses:
        insert_lectures(week_day, course, service, semester_info, calendar_ids)

def process_semester(service, semester_info, courses, calendar_ids):
    # week by week
    week_day = semester_info.firstweek_day
    while week_day <= semester_info.lastweek_day:
        if week_day != semester_info.breakweek_day:
            process_week(week_day, service, semester_info, courses, calendar_ids)
        week_day += timedelta(weeks=1)

def create_calendars(service, courses):
    calendar_ids = {}
    for course in courses:
        calendar = create_calendar_body(course.name)
        response_cal = service.calendars().insert(body=calendar).execute()
        calendar_ids[course.name] = response_cal['id']
    return calendar_ids

def main():
    # service = login(client_id, client_secret)
    service = None

    try:
        # calendar_ids = create_calendars(service, courses)
        # process_semester(service, semester_info, courses, calendar_ids)
        process_semester(service, semester_info, courses, {})
    
    except AccessTokenRefreshError:
        print('The credentials have been revoked or expired, please re-run the application to re-authorize')

if __name__ == '__main__':
    main()
