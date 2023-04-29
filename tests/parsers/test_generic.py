import json
import xml.etree.ElementTree as ET
from unittest.mock import patch

from remindme.parsers.generic import (get_gpt_email_response,
                                      get_gpt_standard_response,
                                      openai_standard)


def test_get_gpt_standard_response():
    prompt = "What is the weather like today?"

    expected_response = "The weather is sunny."

    # Mock the openai.ChatCompletion.create() function
    with patch("remindme.parsers.generic.openai.ChatCompletion.create") as mock_create:
        # Configure the mock response
        mock_response = {"choices": [{"message": {"content": expected_response}}]}
        mock_create.return_value = mock_response

        response = get_gpt_standard_response(prompt)

    # Assert the response matches the expected output
    assert response == expected_response


def test_get_gpt_email_response():
    prompt = (
        "Compose an email with the subject 'Meeting' and body 'Discussion at 2 PM.'"
    )

    expected_response = {"subject_line": "Meeting", "body": "Discussion at 2 PM."}

    # Mock the openai.ChatCompletion.create() function
    with patch("remindme.parsers.generic.openai.ChatCompletion.create") as mock_create:
        # Configure the mock response
        mock_response = {
            "choices": [{"message": {"content": json.dumps(expected_response)}}]
        }
        mock_create.return_value = mock_response

        response = get_gpt_email_response(prompt)

    # Assert the response matches the expected output
    assert response == expected_response


def test_openai_standard():
    message_body = "openai, what is the capital of France?"

    expected_response = "The capital of France is Paris."

    # Mock the openai.ChatCompletion.create() function
    with patch("remindme.parsers.generic.openai.ChatCompletion.create") as mock_create:
        # Configure the mock response
        mock_response = {"choices": [{"message": {"content": expected_response}}]}
        mock_create.return_value = mock_response

        response = openai_standard(message_body)

    # Assert the response matches the expected output
    root = ET.fromstring(str(response))
    assert root.find("Message").text == expected_response
