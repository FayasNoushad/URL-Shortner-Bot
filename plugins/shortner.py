from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyshorteners import Shortener

BITLY_API = os.environ["BITLY_API"]

@FayasNoushad.on_message(filters.private & filters.regex(r'https?://[^\s]+'))
async def short(bot, update):
    link = update.matches[0].group(0)
    shorten_urls = "**--Shorted URLs--**\n"
    
    if BITLY_API:
        try:
            s = Shortener(api_key=BITLY_API)
            url = s.bitly.short(link)
            shorten_urls += f"\n**Bit.ly :-** {url}"
        except Exception as error:
            print(error)
