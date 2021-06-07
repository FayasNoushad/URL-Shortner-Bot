from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyshorteners import Shortener

@FayasNoushad.on_message(filters.private & filters.regex(r'https?://[^\s]+'))
async def short(bot, update):
    link = update.matches[0].group(0)
    shorten_urls = "**--Shorted URLs--**\n"
