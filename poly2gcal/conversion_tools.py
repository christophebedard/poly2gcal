"""Module for JSON dictionaries conversion tools."""

from datetime import timedelta
from typing import Dict
from typing import List

from .time_tools import timedelta_from_class_duration
from .time_tools import timedelta_from_day_and_time
from .time_tools import to_date


def convert_courses(
    courses_json: List[Dict],
) -> List[Dict]:
    """
    Convert input data for courses from JSON to objects when necessary
    """
    courses = []
    for course_json in courses_json:
        course = {}
        course['name'] = course_json['name']
        course['id'] = course_json['id']

        lectures = []
        for lecture_json in course_json['lectures']:
            lecture = {}
            lecture['start'] = timedelta_from_day_and_time(lecture_json['day'], lecture_json['start'])
            lecture['duration'] = timedelta_from_class_duration(int(lecture_json['duration']))
            lecture['room'] = lecture_json['room']
            lectures.append(lecture)
        course['lectures'] = lectures

        lab_json = course_json['lab']
        lab = {}
        lab['start'] = timedelta_from_day_and_time(lab_json['day'], lab_json['start'])
        lab['duration'] = timedelta_from_class_duration(int(lab_json['duration']))
        lab['room'] = lab_json['room']
        lab['week'] = '' if 'week' not in lab_json else lab_json['week']
        course['lab'] = lab

        courses.append(course)
    return courses


def convert_semester_info(
    semester_info: Dict,
) -> None:
    """
    Convert input data for semester info from JSON to objects when necessary
    """
    semester_info['firstweek_day'] = to_date(semester_info['firstweek_day'])
    semester_info['first_day'] = semester_info['firstweek_day'] if ('first_day' not in semester_info or not semester_info['first_day']) else to_date(semester_info['first_day'])
    semester_info['lastweek_day'] = to_date(semester_info['lastweek_day'])
    semester_info['last_day'] = (semester_info['lastweek_day'] + timedelta(days=4)) if ('last_day' not in semester_info or not semester_info['last_day']) else to_date(semester_info['last_day'])
    semester_info['breakweek_day'] = to_date(semester_info['breakweek_day'])
    semester_info['holidays'] = [to_date(day) for day in semester_info['holidays']] if 'holidays' in semester_info else []
    semester_info['alt_exceptions'] = [to_date(day) for day in semester_info['alt_exceptions']] if 'alt_exceptions' in semester_info else []
