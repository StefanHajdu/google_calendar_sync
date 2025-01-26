import datetime
import os.path

import time
from tenacity import retry, wait_random_exponential, retry_if_exception_type

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]


"""Shows basic usage of the Google Calendar API.
Prints the start and name of the next 10 events on the user's calendar.
"""
creds = None
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json",
            SCOPES,
        )
        creds = flow.run_local_server(port=0)


def list_upcomming_n_events(n):
    try:
        service = build("calendar", "v3", credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
        print(f"Getting the upcoming {n} events")
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=now,
                maxResults=n,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            print("No upcoming events found.")
            return []

        return events

        # Prints the start and name of the next n events
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            print(event)
            print(start, event["summary"])
            print()

    except HttpError as error:
        print(f"An error occurred: {error}")


def insert_calendar_events(calendar_events):

    @retry(
        retry=retry_if_exception_type(HttpError),
        wait=wait_random_exponential(multiplier=1, max=60),
    )
    def import_event(e):
        created_e = service.events().insert(calendarId="primary", body=e).execute()
        print(f"Event created: {created_e.get('htmlLink')}")

    service = build("calendar", "v3", credentials=creds)
    for e in calendar_events:
        import_event(e)


def detele_events():

    @retry(
        retry=retry_if_exception_type(HttpError),
        wait=wait_random_exponential(multiplier=1, max=60),
    )
    def delete_event(e):
        service.events().delete(
            calendarId="primary", eventId=f"{e["id"]}", sendNotifications=False
        ).execute()
        print("Zber deleted")

    events = list_upcomming_n_events(150)
    print(len(events))

    service = build("calendar", "v3", credentials=creds)
    for e in events:
        if e["summary"].startswith("Zber"):
            delete_event(e)
