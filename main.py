import os
from pyrogram import Client

import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

FayasNoushad = Client(
    "URL-Shortner-Bot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"],
    plugins = dict(
        root="plugins"
    )
)

if __name__ == "__main__":
    FayasNoushad.run()
