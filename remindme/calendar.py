from dataclasses import dataclass
from datetime import datetime


@dataclass
class Event:
    event: dict

    @property
    def start(self):
        if "dateTime" in self.event["start"].keys():
            datetime_string = self.event["start"]["dateTime"]
            dt_object = datetime.fromisoformat(datetime_string)
            return dt_object.strftime("%A %Y-%m-%d @ %H:%M")
        elif "date" in self.event["start"].keys():
            datetime_string = self.event["start"]["date"]
            dt_object = datetime.strptime(datetime_string, "%Y-%m-%d")
            return dt_object.strftime("%A, %Y-%m-%d")

    @property
    def end(self):
        if "dateTime" in self.event["end"].keys():
            datetime_string = self.event["end"]["dateTime"]
            dt_object = datetime.fromisoformat(datetime_string)
            return dt_object.strftime("%A %Y-%m-%d @ %H:%M")

    @property
    def summary(self):
        return self.event["summary"]

    @property
    def all_day(self):
        return "date" in self.event["start"]


# Function to schedule an event on Google Calendar
def schedule_event(calendar_service, event):
    created_event = (
        calendar_service.events()
        .insert(calendarId="chansoosong@gmail.com", body=event)
        .execute()
    )
    return created_event


# Function to query events on Google Calendar
def query_calendar(calendar_service, events):
    events.pop("classification")
    print(events)
    return (
        calendar_service.events()
        .list(calendarId="chansoosong@gmail.com", **events)
        .execute()
    )
