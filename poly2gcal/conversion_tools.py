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

"""Module for JSON dictionaries conversion tools."""

from datetime import timedelta
from typing import Dict
from typing import List

from .time_tools import monday_of_same_week
from .time_tools import timedelta_from_class_duration
from .time_tools import timedelta_from_day_and_time
from .time_tools import to_date


def convert_courses(
    courses_json: List[Dict],
) -> List[Dict]:
    """
    Convert input data for courses from JSON to objects when necessary.

    :param courses_json: the list of courses
    :return: the list of converted courses
    """
    courses = []
    for course_json in courses_json:
        course = {}
        course['name'] = course_json['name']
        course['id'] = course_json.get('id', '')

        lectures = []
        for lecture_json in course_json['lectures']:
            lecture = {}
            lecture['start'] = timedelta_from_day_and_time(
                lecture_json['day'],
                lecture_json['start'],
            )
            lecture['duration'] = timedelta_from_class_duration(int(lecture_json['duration']))
            lecture['room'] = lecture_json.get('room', '')
            lecture['description'] = lecture_json.get('description', '')
            lectures.append(lecture)
        course['lectures'] = lectures

        labs = []
        for lab_json in course_json['labs']:
            lab = {}
            lab['start'] = timedelta_from_day_and_time(lab_json['day'], lab_json['start'])
            lab['duration'] = timedelta_from_class_duration(int(lab_json['duration']))
            lab['room'] = lab_json.get('room', '')
            lab['description'] = lab_json.get('description', '')
            lab['week'] = lab_json.get('week', '')
            labs.append(lab)
        course['labs'] = labs

        courses.append(course)
    return courses


def convert_semester_info(
    semester_info: Dict,
) -> None:
    """
    Convert input data for semester info from JSON to objects when necessary.

    This is done in-place, i.e. updating the same dict.

    :param semester_info: the semester info to convert
    """
    semester_info['first_day'] = to_date(semester_info['first_day'])
    semester_info['firstweek_day'] = monday_of_same_week(semester_info['first_day'])
    semester_info['last_day'] = to_date(semester_info['last_day'])
    semester_info['lastweek_day'] = monday_of_same_week(semester_info['last_day'])
    semester_info['breakweek_day'] = to_date(semester_info['breakweek_day'])
    semester_info['holidays'] = [to_date(day) for day in semester_info.get('holidays', [])]
    semester_info['alt_exceptions'] = [to_date(day) for day in semester_info.get('alt_exceptions', [])]
    print('firstweek_day=', semester_info['firstweek_day'])
    print('first_day=', semester_info['first_day'])
    print('lastweek_day=', semester_info['lastweek_day'])
    print('last_day=', semester_info['last_day'])
