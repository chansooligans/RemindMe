# %%
import json
from datetime import datetime

import openai
import pytz
from django.core.mail import send_mail
from django.http import HttpResponse
from twilio.twiml.messaging_response import MessagingResponse

prompt = "Do I have any reminders on my schedule today?"

messages = [
    {
        "role": "system",
        "content": "You are an AI assistant that helps with scheduling and reminders.",
    },
    {"role": "user", "content": prompt},
    {
        "role": "system",
        "content": """
            Classify the request as one of the following:
            - "schedule"
            - "reminder"
            - "calendar_query"
            - "reminder_query"
            
            Do not include explanations, only respond with the classification label.
            The classification is:
        """,
    },
]

response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
response["choices"][0]["message"]["content"]


# %%
prompt = "Are there any birthdays coming up?"

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
            The goal is to parse the prompt into a JSON object to send to an API.
            Do not include any explanations, only provide a  RFC8259 compliant JSON response following this format without deviation
            and make sure all keys are included in the object. Make sure the start time is still in Eastern Daylight Time.
            ```
            {
                "timeMin": "2023-04-16T09:00:00-04:00", # the minimum time to query
                "timeMax": "2023-04-16T09:00:00-04:00", # the maximum time to query
                "maxResults": 20, # use 20 as default
                "q": "" # Free text search terms to find events that match these terms. Add similar search terms comma separated that might help search.
            }
            ```
            The JSON response:
        """,
    },
]

response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
response = json.loads(response["choices"][0]["message"]["content"])
response["singleEvents"] = True
response["orderBy"] = "startTime"
response

# %%

# %%
