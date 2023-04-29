import json
from datetime import datetime

import openai
import pytz
from django.core.mail import send_mail
from django.http import HttpResponse
from twilio.twiml.messaging_response import MessagingResponse


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
        return "email has been delivered"

    else:  # otherwise text message
        response = get_gpt_standard_response(message_body.split("openai,")[-1])
        resp = MessagingResponse()
        resp.message(response)
        return resp
