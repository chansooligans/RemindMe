import openai
from datetime import datetime
import json
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
            "content": f"""
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

    print(messages)

    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

    print(response)
    response = json.loads(response["choices"][0]["message"]["content"])
    print("parsed:", response)

    for k in ["summary", "location", "description", "start", "end", "classification"]:
        if k not in response.keys():
            response[k] = ""
    if isinstance(response["classification"], list):
        response["classification"] = response["classification"][0]

    return response


def get_gpt_standard_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant. Please ensure your response is less than 320 characters.",
            },
            {"role": "user", "content": prompt},
        ],
    )

    return response["choices"][0]["message"]["content"]


def get_gpt_email_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant. You will be responding to a user prompt with a title and body.",
            },
            {"role": "user", "content": prompt},
            {
                "role": "system",
                "content": """
                Do not include any explanations, only provide a  RFC8259 compliant JSON object following this format without deviation
                and make sure all keys are included in the object:
                ```
                {
                    "subject_line": "[title here]",
                    "body": "[body here]",
                }
                ```
                The JSON object:
            """,
            },
        ],
    )

    print(response)

    response = json.loads(response["choices"][0]["message"]["content"])

    for k in ["subject_line", "body"]:
        if k not in response.keys():
            response[k] = ""

    return response


def openai_standard(message_body):
    if message_body.startswith("openai, email"):
        response = get_gpt_email_response(message_body.split("openai, email")[-1])
        send_mail(
            response["subject_line"],
            response["body"],
            "chansoosong@gmail.com",
            ["chansoosong@gmail.com"],
            fail_silently=False,
        )
        return HttpResponse("email has been delivered")

    else:  # otherwise text message
        response = get_gpt_standard_response(message_body.split("openai,")[-1])
        resp = MessagingResponse()
        resp.message(response)
        return HttpResponse(str(resp))
