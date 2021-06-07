import os
from pyrogram import Client 

FayasNoushad = Client(
    "URL-Shortner-Bot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"],
    plugins = dict(root="plugins")
)

FayasNoushad.run()
