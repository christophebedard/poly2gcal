"""Module for the main poly2gcal logic."""

import json
from datetime import datetime
from datetime import timedelta
from typing import Dict
from typing import List

from apiclient.discovery import Resource

from oauth2client.client import AccessTokenRefreshError

from .conversion_tools import convert_courses
from .conversion_tools import convert_semester_info
from .gcal import create_calendar_body
from .gcal import create_event_body
from .gcal import login
from .time_tools import date_to_datetime
from .weekdates_intervals import get_interval


def is_in_semester(
    date_time: datetime,
    semester_info: Dict,
) -> bool:
    """
    Check if a datetime is within the first and last days of the semester.

    :param date_time: the date/time
    :param semester_info: the semester info
    :return True if the given date/time is in the semester, False otherwise
    """
    return semester_info['first_day'] <= date_time.date() <= semester_info['last_day']


def is_holiday(
    date: datetime,
    semester_info: Dict,
) -> bool:
    """
    Check if a date is a holiday.

    :param date: the date/time
    :param semester_info: the semester info
    :return True if the given date/time is a holiday, False otherwise
    """
    return date.date() in semester_info['holidays']


def is_alt_week_exception(
    date_time: datetime,
    semester_info: Dict,
) -> bool:
    """
    Check if a datetime corresponds to an exception to the usual week alternation rule.

    i.e. Monday might be B1 while the rest of the week is B2.

    :param date: the date/time
    :param semester_info: the semester info
    :return True if the given date/time is an exception, False otherwise
    """
    return date_time.date() in semester_info['alt_exceptions']


def insert_event(
    service: Resource,
    course_name: str,
    calendar_ids: Dict,
    body: Dict,
    test: bool = False,
) -> None:
    """Insert an event (but only if the test flag is not enabled)."""
    print('EVENT:\n' + repr(body))
    if not test:
        service.events().insert(
            calendarId=calendar_ids[course_name],
            body=body,
        ).execute()


def insert_calendar(
    service: Resource,
    body: Dict,
    course_name: str,
    calendar_ids: Dict,
    test: bool = False,
) -> None:
    """Insert a calendar (but only if the test flag is not enabled)."""
    print('CALENDAR:\n' + repr(body))
    if not test:
        response_cal = service.calendars().insert(
            body=body,
        ).execute()
        calendar_ids[course_name] = response_cal['id']


def check_lab(
    week_day: datetime,
    week_alt_lab: str,
    course_name: str,
    lab: Dict,
    service: Resource,
    semester_info: Dict,
    calendar_ids: Dict,
    test: bool = False,
    checklist: bool = False,
) -> None:
    """Check if there is a lab in a given week and insert if there is."""
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
                event_name = f'Lab - {course_name}'
                event = create_event_body(
                    event_name,
                    lab['room'],
                    start,
                    end,
                )
                insert_event(
                    service,
                    course_name,
                    calendar_ids,
                    event,
                    test=test,
                )
            else:
                print('Lab {} done'.format(course_name))


def insert_labs(
    week_day: datetime,
    week_alt_lab: str,
    course_name: str,
    labs: List[Dict],
    service: Resource,
    semester_info: Dict,
    calendar_ids: Dict,
    test: bool = False,
    checklist: bool = False,
) -> None:
    """Insert labs for a course for a given week."""
    for lab in labs:
        check_lab(
            week_day,
            week_alt_lab,
            course_name,
            lab,
            service,
            semester_info,
            calendar_ids,
            test=test,
            checklist=checklist,
        )


def insert_lectures(
    week_day: datetime,
    course_name: str,
    lectures: List[Dict],
    service: Resource,
    semester_info: Dict,
    calendar_ids: Dict,
    test: bool = False,
) -> None:
    """Insert lectures for a course for a given week."""
    for lecture in lectures:
        start = date_to_datetime(week_day) + lecture['start']
        if is_in_semester(start, semester_info) and not is_holiday(start, semester_info):
            end = start + lecture['duration']
            event_name = f'Cours - {course_name}'
            event = create_event_body(
                event_name,
                lecture['room'],
                start,
                end,
            )
            insert_event(
                service,
                course_name,
                calendar_ids,
                event,
                test=test,
            )


def process_week(
    week_day: datetime,
    week_alt_lab: str,
    service: Resource,
    semester_info: Dict,
    courses: List[Dict],
    calendar_ids: Dict,
    test: bool = False,
    checklist: bool = False,
) -> None:
    """Process all courses (lectures and labs) for a given week."""
    for course in courses:
        course_name = course['name']
        insert_labs(
            week_day,
            week_alt_lab,
            course_name,
            course['labs'],
            service,
            semester_info,
            calendar_ids,
            test=test,
            checklist=checklist,
        )
        if not checklist:
            insert_lectures(
                week_day,
                course_name,
                course['lectures'],
                service,
                semester_info,
                calendar_ids,
                test=test,
            )


def flip_alt_week(
    alt_week: str,
) -> str:
    """Flip an alternate week value."""
    return 'B2' if alt_week == 'B1' else 'B1'


def process_semester(
    service: Resource,
    semester_info: Dict,
    courses: List[Dict],
    calendar_ids,
    test: bool = False,
    checklist: bool = False,
) -> None:
    """Process the whole semester, adding lectures and labs."""
    # week by week
    week_day = semester_info['firstweek_day']
    week_alt_lab = 'B1'
    while week_day <= semester_info['lastweek_day']:
        if checklist:
            print(get_interval(week_day))
        if week_day != semester_info['breakweek_day']:
            process_week(
                week_day,
                week_alt_lab,
                service,
                semester_info,
                courses,
                calendar_ids,
                test=test,
                checklist=checklist,
            )
            week_alt_lab = flip_alt_week(week_alt_lab)
        week_day += timedelta(weeks=1)


def create_calendars(
    service: Resource,
    courses: List[Dict],
    test: bool = False,
) -> Dict:
    """Create a calendar for each course."""
    calendar_ids = {}
    for course in courses:
        course_name = course['name']
        calendar = create_calendar_body(course_name)
        insert_calendar(
            service,
            calendar,
            course_name,
            calendar_ids,
            test=test,
        )
    return calendar_ids


def main(
    data_file_path: str,
    test: bool,
    checklist: bool,
) -> None:
    """
    Get API service and process input data.

    :param test: whether to only preview requests and not actually send them
    :param checklist: whether to generate tasks checklists
    """
    service = login() if not test else None

    with open(data_file_path) as f:
        data = json.load(f)

    semester_info = data['semester_info']
    convert_semester_info(semester_info)
    courses = convert_courses(data['courses'])

    try:
        calendar_ids = create_calendars(service, courses, test=test) if not checklist else None
        process_semester(
            service,
            semester_info,
            courses,
            calendar_ids,
            test=test,
            checklist=checklist,
        )
    except AccessTokenRefreshError:
        print((
            'The credentials have been revoked or expired. '
            'Please re-run the application to re-authorize.'
        ))
