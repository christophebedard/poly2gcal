#!/usr/bin/python3

## Stuff to send info to Google Calendar

import httplib2
import sys

from apiclient.discovery import build
from oauth2client import tools
from oauth2client.file import Storage
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import OAuth2WebServerFlow

from data import *

client_id = ''
client_secret = ''
scope = 'https://www.googleapis.com/auth/calendar'

def login():
    storage = Storage('credentials.dat')
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        flow = OAuth2WebServerFlow(client_id, client_secret, scope)
        credentials = tools.run_flow(flow, storage, tools.argparser.parse_args())
    
    http = httplib2.Http()
    http = credentials.authorize(http)

    return build('calendar', 'v3', http=http)

def create_calendars(service, courses):
    calendar_ids = {}

    for course in courses:
        calendar = {
            'summary': course.name,
            'timeZone': 'America/Toronto'
        }
        response_cal = service.calendars().insert(body=calendar).execute()
        calendar_ids[course.name] = response_cal['id']
    
    return calendar_ids

def main():
    service = login()

    try:
        calendar_ids = create_calendars(service, courses)
    
    except AccessTokenRefreshError:
        print('The credentials have been revoked or expired, please re-run the application to re-authorize')

if __name__ == '__main__':
    main()
