# %%
if get_ipython() is not None:
    get_ipython().run_line_magic("load_ext", "autoreload")
    get_ipython().run_line_magic("autoreload", "2")
from remindme import config, parsers

config.setup()

# %%
message_body = """
    openai, what is 2+2?
""".strip()

# %%
if message_body.startswith("openai"):
    result = parsers.openai_standard(message_body)
    str(result)

# %%
if not message_body.startswith("openai"):
    parsed_event = parsers.get_gpt4_schedule_response(message_body)


# %%
if parsed_event["classification"] == "schedule":
    calendar.schedule_event(calendar_service, parsed_event)

    # Start our TwiML response
    resp = MessagingResponse()

    dt = datetime.fromisoformat(parsed_event["start"]["dateTime"])
    start_time = dt.strftime("%Y-%m-%d at %-I:%M%p")

    # Determine the right reply for this message
    resp.message(
        f"""Your event '{parsed_event["summary"]}' on {start_time} is scheduled"""
    )

    return HttpResponse(str(resp))

elif parsed_event["classification"] == "reminder":
    print(parsed_event.keys())
    event = ScheduledEvent(
        summary=parsed_event["summary"],
        location=parsed_event["location"],
        description=parsed_event["description"],
        start_time=parsed_event["start"]["dateTime"],
        end_time=parsed_event["end"]["dateTime"],
        phone_number=sender_phone_number,
    )
    event.save()
    print("saved")

    # Start our TwiML response
    resp = MessagingResponse()

    dt = datetime.fromisoformat(parsed_event["start"]["dateTime"])
    start_time = dt.strftime("%Y-%m-%d at %-I:%M%p")

    # Determine the right reply for this message
    resp.message(
        f"""Your reminder '{parsed_event["summary"]}' on {start_time} is scheduled"""
    )

    return HttpResponse(str(resp))
