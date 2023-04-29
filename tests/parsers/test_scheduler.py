import json
from unittest.mock import patch

from remindme.parsers.scheduler import get_gpt4_schedule_response


def test_get_gpt4_schedule_response():
    prompt = "Schedule a meeting for tomorrow at 10 AM"

    expected_response = {
        "summary": "Meeting",
        "location": "Conference Room",
        "description": "Discussion on project updates",
        "start": {"dateTime": "2023-04-30T10:00:00-04:00"},
        "end": {"dateTime": "2023-04-30T11:00:00-04:00"},
        "classification": "schedule",
    }

    # Mock the openai.ChatCompletion.create() function
    with patch(
        "remindme.parsers.scheduler.openai.ChatCompletion.create"
    ) as mock_create:
        # Configure the mock response
        mock_response = {
            "choices": [{"message": {"content": json.dumps(expected_response)}}]
        }
        mock_create.return_value = mock_response

        response = get_gpt4_schedule_response(prompt)

    # Assert the response matches the expected output
    assert response == expected_response
