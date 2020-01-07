"""Module for Google Calendar helpers."""

from datetime import datetime
import httplib2
import sys
from typing import Dict

from apiclient.discovery import build
from apiclient.discovery import Resource
from oauth2client import tools
from oauth2client.file import Storage
from oauth2client.client import flow_from_clientsecrets


def login(
    scope: str = 'https://www.googleapis.com/auth/calendar',
    secrets_file_path: str = 'client_secrets.json',
) -> Resource:
    storage = Storage('credentials.dat')
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
    return {
        'summary': title,
        'timeZone': timezone,
    }


def create_event_body(
    event_name: str,
    location: str,
    start: datetime,
    end: datetime,
    timezone: str = 'America/Toronto',
) -> Dict:
    return {
        'summary': event_name,
        'location': location,
        'start': {
            'dateTime': start.isoformat(),
            'timeZone': timezone,
        },
        'end': {
            'dateTime': end.isoformat(),
            'timeZone': timezone,
        },
    }
