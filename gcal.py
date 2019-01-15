## Google Calendar helpers

import httplib2
import sys

from apiclient.discovery import build
from oauth2client import tools
from oauth2client.file import Storage
from oauth2client.client import flow_from_clientsecrets


SCOPE = 'https://www.googleapis.com/auth/calendar'
SECRETS_PATH = 'client_secrets.json'
TIMEZONE = 'America/Toronto'

def login():
    storage = Storage('credentials.dat')
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        flow = flow_from_clientsecrets(SECRETS_PATH, SCOPE)
        credentials = tools.run_flow(flow, storage, tools.argparser.parse_args())
    
    http = httplib2.Http()
    http = credentials.authorize(http)

    return build('calendar', 'v3', http=http)

def create_calendar_body(title):
    return {
                'summary': title,
                'timeZone': TIMEZONE
            }

def create_event_body(event_name, location, start, end):
    return {
                'summary': event_name,
                'location': location,
                'start': {
                    'dateTime': start.isoformat(),
                    'timeZone': TIMEZONE
                },
                'end': {
                    'dateTime': end.isoformat(),
                    'timeZone': TIMEZONE
                }
            }
