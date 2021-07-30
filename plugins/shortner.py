# Made with python3
# (C) @FayasNoushad
# Copyright permission under MIT License
# All rights reserved by FayasNoushad
# License -> https://github.com/FayasNoushad/URL-Shortner-Bot/blob/main/LICENSE

import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent
from pyshorteners import Shortener

BITLY_API = os.environ.get("BITLY_API", "")
CUTTLY_API = os.environ.get("CUTTLY_API", "")
SHORTCM_API = os.environ.get("SHORTCM_API", "")

BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton(text='⚙ Join Updates Channel ⚙', url='https://telegram.me/FayasNoushad')
        ]]
    )

@Client.on_message(filters.private & filters.regex(r'https?://[^\s]+'))
async def reply_shortens(bot, update):
    message = await update.reply_text(
        text="`Analysing your link...`",
        disable_web_page_preview=True,
        quote=True
    )
    link = update.matches[0].group(0)
    shorten_urls = await short(link)
    await message.edit_text(
        text=shorten_urls,
        reply_markup=BUTTONS,
        disable_web_page_preview=True
    )

@Client.on_inline_query(filters.regex(r'https?://[^\s]+'))
async def inline_short(bot, update):
    link = update.matches[0].group(0)
    shorten_urls = await short(link)
    answers = [
        InlineQueryResultArticle(
            title="Short Links",
            description=update.query,
            input_message_content=InputTextMessageContent(
                message_text=shorten_urls,
                disable_web_page_preview=True
            ),
            reply_markup=BUTTONS
        )
    ]
    await bot.answer_inline_query(
        inline_query_id=update.id,
        results=answers
    )

async def short(link):
    shorten_urls = "**--Shorted URLs--**\n"
    
    # Bit.ly shorten
    if BITLY_API:
        try:
            s = Shortener(api_key=BITLY_API)
            url = s.bitly.short(link)
            shorten_urls += f"\n**Bit.ly :-** {url}"
        except Exception as error:
            print(f"Bit.ly error :- {error}")
    
    # Chilp.it shorten
    try:
        s = Shortener()
        url = s.chilpit.short(link)
        shorten_urls += f"\n**Chilp.it :-** {url}"
    except Exception as error:
        print(f"Chilp.it error :- {error}")
    
    # Clck.ru shorten
    try:
        s = Shortener()
        url = s.clckru.short(link)
        shorten_urls += f"\n**Clck.ru :-** {url}"
    except Exception as error:
        print(f"Click.ru error :- {error}")
    
    # Cutt.ly shorten
    if CUTTLY_API:
        try:
            s = Shortener(api_key=CUTTLY_API)
            url = s.cuttly.short(link)
            shorten_urls += f"\n**Cutt.ly :-** {url}"
        except Exception as error:
            print(f"Cutt.ly error :- {error}")
    
    # Da.gd shorten
    try:
        s = Shortener()
        url = s.dagd.short(link)
        shorten_urls += f"\n**Da.gd :-** {url}"
    except Exception as error:
        print(f"Da.gd error :- {error}")
    
    # Is.gd shorten
    try:
        s = Shortener()
        url = s.isgd.short(link)
        shorten_urls += f"\n**Is.gd :-** {url}"
    except Exception as error:
        print(f"Is.gd error :- {error}")
    
    # Osdb.link shorten
    try:
        s = Shortener()
        url = s.osdb.short(link)
        shorten_urls += f"\n**Osdb.link :-** {url}"
    except Exception as error:
        print(f"Osdb.link error :- {error}")
    
    # Ow.ly shorten
    try:
        s = Shortener()
        url = s.owly.short(link)
        shorten_urls += f"\n**Ow.ly :-** {url}"
    except Exception as error:
        print(f"Ow.ly error :- {error}")
    
    # Po.st shorten
    try:
        s = Shortener()
        url = s.post.short(link)
        shorten_urls += f"\n**Po.st :-** {url}"
    except Exception as error:
        print(f"Po.st error :- {error}")
    
    # Qps.ru shorten
    try:
        s = Shortener()
        url = s.qpsru.short(link)
        shorten_urls += f"\n**Qps.ru :-** {url}"
    except Exception as error:
        print(f"Qps.ru error :- {error}")
    
    # Short.cm shorten
    if SHORTCM_API:
        try:
            s = Shortener(api_key=SHORTCM_API)
            url = s.shortcm.short(link)
            shorten_urls += f"\n**Short.cm :-** {url}"
        except Exception as error:
            print(f"Short.cm error :- {error}")
    
    # TinyURL.com shorten
    try:
        s = Shortener()
        url = s.tinyurl.short(link)
        shorten_urls += f"\n**TinyURL.com :-** {url}"
    except Exception as error:
        print(f"TinyURL.com error :- {error}")
    
    # NullPointer shorten
    try:
        s = Shortener(domain='https://0x0.st')
        url = s.nullpointer.short(link)
        shorten_urls += f"\n**0x0.st :-** {url}"
    except Exception as error:
        print(f"NullPointer error :- {error}")
    
    # Send the text
    try:
        shorten_urls += "\n\nMade by @FayasNoushad"
        return shorten_urls
    except Exception as error:
        return error
