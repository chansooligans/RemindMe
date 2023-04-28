from pathlib import Path
from twilio.rest import Client
from googleapiclient.discovery import build
import yaml

try:
    with open(
        "/home/chansoo/projects/apps.chansoo/apps/twilioapp/api.yaml", "r"
    ) as config_file:
        config = yaml.safe_load(config_file)
except:
    with open(
        "/home/bitnami/projects/apps.chansoo/apps/twilioapp/api.yaml", "r"
    ) as config_file:
        config = yaml.safe_load(config_file)

OPENAI_API_KEY = config["openai"]["api_key"]
TWILIO_ACCOUNT_SID = config["twilio"]["account_sid"]
TWILIO_AUTH_TOKEN = config["twilio"]["auth_token"]
TWILIO_PHONE_NUMBER = config["twilio"]["phone_number"]

twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


def send_reminder(phone_number, message):
    twilio_client.messages.create(
        body=message,
        from_=TWILIO_PHONE_NUMBER,
        to=phone_number,
    )
