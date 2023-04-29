import openai
import yaml
from twilio.rest import Client
from google.oauth2 import service_account
from googleapiclient.discovery import build


def setup():
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

    openai.api_key = OPENAI_API_KEY
    twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    try:
        GOOGLE_SERVICE_ACCOUNT_FILE = (
            f"/home/chansoo/projects/apps.chansoo/apps/twilioapp/credentials.json"
        )
        google_credentials = service_account.Credentials.from_service_account_file(
            GOOGLE_SERVICE_ACCOUNT_FILE
        )
        calendar_service = build("calendar", "v3", credentials=google_credentials)
    except:
        GOOGLE_SERVICE_ACCOUNT_FILE = (
            f"/home/bitnami/projects/apps.chansoo/apps/twilioapp/credentials.json"
        )
        google_credentials = service_account.Credentials.from_service_account_file(
            GOOGLE_SERVICE_ACCOUNT_FILE
        )
        calendar_service = build("calendar", "v3", credentials=google_credentials)

    return calendar_service
