import datetime
from dataclasses import dataclass

import googleapiclient
from django.db import models
from django.http import HttpResponse
from twilio.twiml.messaging_response import MessagingResponse

from remindme import calendar, parsers


@dataclass
class ScheduleParser:
    message_body: str

    def parse(self):
        return parsers.scheduler.get_gpt4_schedule_response(self.message_body)


@dataclass
class OpenAIParser:
    message_body: str

    def parse(self):
        return parsers.generic.openai_standard(self.message_body)


@dataclass
class MessageParser:
    message_body: str
    _type: str = None

    def __post_init__(self):
        if self.message_body.startswith("openai"):
            self._type = "generic"
            self.parser = OpenAIParser(self.message_body)
        else:
            self._type = "scheduler"
            self.parser = ScheduleParser(self.message_body)

    def parse_message(self):
        return self.parser.parse()


@dataclass
class RequestHandler:
    parsed: str
    calendar_service: googleapiclient.discovery.Resource
    ScheduledEvent: models.Model
    sender_phone_number: str

    def process_request(self):
        if self.parsed["classification"] == "schedule":
            calendar.schedule_event(self.calendar_service, self.parsed)

            # Start our TwiML response
            resp = MessagingResponse()

            dt = datetime.fromisoformat(self.parsed["start"]["dateTime"])
            start_time = dt.strftime("%Y-%m-%d at %-I:%M%p")

            # Determine the right reply for this message
            resp.message(
                f"""Your event '{self.parsed["summary"]}' on {start_time} is scheduled"""
            )

            return HttpResponse(str(resp))

        elif self.parsed["classification"] == "reminder":
            print(self.parsed.keys())
            event = self.ScheduledEvent(
                summary=self.parsed["summary"],
                location=self.parsed["location"],
                description=self.parsed["description"],
                start_time=self.parsed["start"]["dateTime"],
                end_time=self.parsed["end"]["dateTime"],
                phone_number=self.sender_phone_number,
            )
            event.save()
            print("saved")

            # Start our TwiML response
            resp = MessagingResponse()

            dt = datetime.fromisoformat(self.parsed["start"]["dateTime"])
            start_time = dt.strftime("%Y-%m-%d at %-I:%M%p")

            # Determine the right reply for this message
            resp.message(
                f"""Your reminder '{self.parsed["summary"]}' on {start_time} is scheduled"""
            )

            return HttpResponse(str(resp))
