# %%
from IPython import get_ipython

if get_ipython() is not None:
    get_ipython().run_line_magic("load_ext", "autoreload")
    get_ipython().run_line_magic("autoreload", "2")
from remindme import config, parsers
from remindme.main import MessageHandler

config.setup()

# %%
message_body = """
    schedule an appointment at 4pm to make cups.
""".strip()

# %%
handler = MessageHandler(message_body=message_body)
res = handler.parse_message()
res
