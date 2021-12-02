from pyrogram import Client
from .commands import *
from .admin import *


@Client.on_callback_query()
async def cb_handler(bot, update):
    
    if not await db.is_user_exist(update.from_user.id):
        await db.add_user(update.from_user.id)
    
    if update.data == "home":
        await update.message.edit_text(
            text=START_TEXT.format(update.from_user.mention),
            reply_markup=START_BUTTONS,
            disable_web_page_preview=True
        )
    
    elif update.data == "help":
        await update.message.edit_text(
            text=HELP_TEXT,
            reply_markup=HELP_BUTTONS,
            disable_web_page_preview=True
        )
    
    elif update.data == "about":
        await update.message.edit_text(
            text=ABOUT_TEXT.format((await bot.get_me()).username),
            reply_markup=ABOUT_BUTTONS,
            disable_web_page_preview=True
        )
    
    elif update.data == "settings":
        await display_settings(bot, update, db, cb=True)
    
    elif update.data == "reset":
        await update.message.edit_text(
            text=RESET_TEXT,
            disable_web_page_preview=True,
            reply_markup=RESET_BUTTONS
        )
    
    elif update.data == "confirm_reset":
        await db.delete_user(update.from_user.id)
        await db.add_user(update.from_user.id)
        await update.message.edit_text(
            text="**Settings reset successfully**",
            disable_web_page_preview=True,
            reply_markup=HELP_BUTTONS
        )
    
    elif update.data == "cancel_reset":
        await update.message.edit_text(
            text="**Reset cancelled successfully**",
            disable_web_page_preview=True,
            reply_markup=HELP_BUTTONS
        )
    
    elif update.data == "close":
        await update.message.delete()
    
    elif update.data.startswith("set+"):
        chat_id = update.from_user.id
        domain = update.data.split("+")[1]
        await db.update_domain(update.from_user.id, domain, not await db.allow_domain(chat_id, domain))
        alert_text = f"{domain} settings updated successfully"
        await display_settings(bot, update, db, cb=True)
        await update.answer(text=alert_text)
