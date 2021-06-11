# Made with python3
# (C) @FayasNoushad
# Copyright permission under MIT License
# All rights reserved by FayasNoushad
# License -> https://github.com/FayasNoushad/URL-Shortner-Bot/blob/main/LICENSE

import os
from pyrogram import Client as FayasNoushad
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyshorteners import Shortener

BITLY_API = os.environ.get("BITLY_API", "")
CUTTLY_API = os.environ.get("CUTTLY_API", "")
SHORTCM_API = os.environ.get("SHORTCM_API", "")

BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton(text='⚙ Join Updates Channel ⚙', url='https://telegram.me/FayasNoushad')
        ]]
    )

@FayasNoushad.on_message(filters.private & filters.regex(r'https?://[^\s]+'))
async def short(bot, update):
    message = await update.reply_text(
        text="`Analysing your link...`",
        disable_web_page_preview=True
    )
    
    link = update.matches[0].group(0)
    shorten_urls = "**--Shorted URLs--**\n"
    
    # Bit.ly shorten
    if BITLY_API:
        try:
            s = Shortener(api_key=BITLY_API)
            url = s.bitly.short(link)
            shorten_urls += f"\n**Bit.ly :-** {url}"
        except Exception as error:
            print(error)
    
    # Chilp.it shorten
    try:
        s = Shortener()
        url = s.chilpit.short(link)
        shorten_urls += f"\n**Chilp.it :-** {url}"
    except Exception as error:
        print(error)
    
    # Clck.ru shorten
    try:
        s = Shortener()
        url = s.clckru.short(link)
        shorten_urls += f"\n**Clck.ru :-** {url}"
    except Exception as error:
        print(error)
    
    # Cutt.ly shorten
    if CUTTLY_API:
        try:
            s = Shortener(api_key=CUTTLY_API)
            url = s.cuttly.short(link)
            shorten_urls += f"\n**Cutt.ly :-** {url}"
        except Exception as error:
            print(error)
    
    # Da.gd shorten
    try:
        s = Shortener()
        url = s.dagd.short(link)
        shorten_urls += f"\n**Da.gd :-** {url}"
    except Exception as error:
        print(error)
    
    # Is.gd shorten
    try:
        s = Shortener()
        url = s.isgd.short(link)
        shorten_urls += f"\n**Is.gd :-** {url}"
    except Exception as error:
        print(error)
    
    # Os.db shorten
    try:
        s = Shortener()
        url = s.osdb.short(link)
        shorten_urls += f"\n**Osdb.link :-** {url}"
    except Exception as error:
        print(error)
    
    # Ow.ly shorten
    try:
        s = Shortener()
        url = s.owly.short(link)
        shorten_urls += f"\n**Ow.ly :-** {url}"
    except Exception as error:
        print(error)
    
    # Po.st shorten
    try:
        s = Shortener()
        url = s.post.short(link)
        shorten_urls += f"\n**Po.st :-** {url}"
    except Exception as error:
        print(error)
    
    # Qps.ru shorten
    try:
        s = Shortener()
        url = s.qpsru.short(link)
        shorten_urls += f"\n**Qps.ru :-** {url}"
    except Exception as error:
        print(error)
    
    # Short.cm shorten
    if SHORTCM_API:
        try:
            s = Shortener(api_key=SHORTCM_API)
            url = s.shortcm.short(link)
            shorten_urls += f"\n**Short.cm :-** {url}"
        except Exception as error:
            print(error)
    
    # TinyURL.com shorten
    try:
        s = Shortener()
        url = s.tinyurl.short(link)
        shorten_urls += f"\n**TinyURL.com :-** {url}"
    except Exception as error:
        print(error)
        
    # Send the text
    try:
        shorten_urls += "\n\nMade by @FayasNoushad"
        await message.edit_text(
            text=shorten_urls,
            reply_markup=BUTTONS,
            disable_web_page_preview=True
        )
    except Exception as error:
        print(error)
