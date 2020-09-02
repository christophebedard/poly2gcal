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

"""Module for Google Calendar helpers."""

from datetime import datetime
from typing import Dict

from apiclient.discovery import Resource
from apiclient.discovery import build

import httplib2

from oauth2client import tools
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage


def login(
    scope: str = 'https://www.googleapis.com/auth/calendar',
    secrets_file_path: str = 'client_secrets.json',
    credentials_file_path: str = 'credentials.dat',
) -> Resource:
    """
    Log into the Google calendar API.

    :param scope: the API scope link
    :param secrets_file_path: the path to the secrets file
    :param credentials_file_path: the path to the credentials file for buffering
    :return: the API resource
    """
    storage = Storage(credentials_file_path)
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        flow = flow_from_clientsecrets(secrets_file_path, scope)
        credentials = tools.run_flow(flow, storage, tools.argparser.parse_args())

    http = httplib2.Http()
    http = credentials.authorize(http)

    return build('calendar', 'v3', http=http)


def create_calendar_body(
    title: str,
    timezone: str = 'America/Toronto',
) -> Dict:
    """
    Create calendar body data.

    :param title: the calendar title
    :param timezone: the timezone
    :return: the calenday body
    """
    return {
        'summary': title,
        'timeZone': timezone,
    }


def create_event_body(
    event_name: str,
    location: str,
    description: str,
    start: datetime,
    end: datetime,
    timezone: str = 'America/Toronto',
) -> Dict:
    """
    Create calendar event body data.

    :param event_name: the name of the calendar event
    :param location: the event location
    :param description: the event description
    :param start: the start date/time
    :param end: the end date/time
    :param timezone: the timezone
    :return: the calendar event body
    """
    return {
        'summary': event_name,
        'location': location,
        'description': description,
        'start': {
            'dateTime': start.isoformat(),
            'timeZone': timezone,
        },
        'end': {
            'dateTime': end.isoformat(),
            'timeZone': timezone,
        },
    }
