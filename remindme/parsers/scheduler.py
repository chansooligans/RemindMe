import json
from datetime import datetime

import openai
import pytz
from django.core.mail import send_mail
from django.http import HttpResponse
from twilio.twiml.messaging_response import MessagingResponse


def get_gpt4_schedule_response(prompt):
    messages = [
        {
            "role": "system",
            "content": "You are an AI assistant that helps with scheduling and reminders.",
        },
        {"role": "user", "content": prompt},
        {
            "role": "system",
            "content": f"The current date and time is {datetime.now(pytz.timezone('US/Eastern'))}, Eastern Daylight Time",
        },
        {
            "role": "system",
            "content": """
                Classify the request as one of the following:
                - schedule
                - reminder
            """,
        },
        {
            "role": "system",
            "content": """
                Do not include any explanations, only provide a  RFC8259 compliant JSON response following this format without deviation
                and make sure all keys are included in the object. Make sure the start time is still in Eastern Daylight Time.
                ```
                {
                    "summary": "Google I/O 2015",
                    "location": "800 Howard St., San Francisco, CA 94103",
                    "description": "A chance to hear more about Google\'s developer products.",
                    "start": {
                        "dateTime": "2023-04-16T09:00:00-04:00"
                    },
                    "end": {
                        "dateTime": "2023-04-16T17:00:00-04:00"
                    },
                    "classification": "schedule" or "reminder"
                }
                ```
                The JSON response:
            """,
        },
    ]

    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    response = json.loads(response["choices"][0]["message"]["content"])

    for k in ["summary", "location", "description", "start", "end", "classification"]:
        if k not in response.keys():
            response[k] = ""
    if isinstance(response["classification"], list):
        response["classification"] = response["classification"][0]

    return response
