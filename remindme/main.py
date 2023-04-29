from dataclasses import dataclass
from remindme import parsers


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
class MessageHandler:
    message_body: str

    def __post_init__(self):
        if self.message_body.startswith("openai"):
            self.parser = OpenAIParser(self.message_body)
        else:
            self.parser = ScheduleParser(self.message_body)

    def parse_message(self):
        return self.parser.parse()
