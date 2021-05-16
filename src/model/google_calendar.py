#!/usr/bin/python
# -*- coding:utf-8 -*-

from __future__ import print_function
from datetime import datetime
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


def get_dirpath_project_root(name):
    return os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))),
        name,
    )


class GoogleCalendar:
    def __init__(self):
        scopes = ["https://www.googleapis.com/auth/calendar.readonly"]
        creds = None

        token_path = get_dirpath_project_root("token.json")
        cred_path = get_dirpath_project_root("credentials.json")

        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, scopes)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(cred_path, scopes)
                creds = flow.run_local_server(port=0)
            with open(token_path, "w") as token:
                token.write(creds.to_json())

        self.service = build("calendar", "v3", credentials=creds)

    def get_events(self, calendar_id, max_results):
        now = datetime.utcnow().isoformat() + "Z"
        events_result = (
            self.service.events()
            .list(
                calendarId=calendar_id,
                timeMin=now,
                maxResults=max_results,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            return []

        return [self.format_event(event) for event in events]

    def format_event(self, event):
        summary = event.get("summary", "タイトルなし")
        start_str = event["start"].get("dateTime", event["start"].get("date"))
        end_str = event["end"].get("dateTime", event["end"].get("date"))
        start_datetime = datetime.fromisoformat(start_str)
        end_datetime = datetime.fromisoformat(end_str)

        return {
            "start": start_str,
            "end": end_str,
            "period": self.format_event_period(start_datetime, end_datetime),
            "summary": summary,
        }

    def format_event_period(self, start_datetime, end_datetime):
        start = {
            "date_str": start_datetime.strftime("%m.%d"),
            "time_str": start_datetime.strftime("%H%M"),
        }
        end = {
            "date_str": end_datetime.strftime("%m.%d"),
            "time_str": end_datetime.strftime("%H%M"),
        }

        if start["date_str"] == end["date_str"]:
            return f'{start["date_str"]} {start["time_str"]}-{end["time_str"]}'
        elif start["time_str"] == "0000" and end["time_str"] == "0000":
            return f'{start["date_str"]}-{end["date_str"]}'
        else:
            return f'{start["date_str"]} {start["time_str"]}-{end["date_str"]} {end["time_str"]}'
