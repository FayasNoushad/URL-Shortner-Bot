import os
import time
import math
import json
import string
import random
import traceback
import asyncio
import datetime
import motor.motor_asyncio
import aiofiles
from io import BytesIO
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid, UserNotParticipant, UserBannedInChannel
from pyrogram.errors.exceptions.bad_request_400 import PeerIdInvalid


class Database:
        
    def __init__(
        self,
        url=os.environ.get("DATABASE"),
        database_name="URLShortBot"
    ):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(url)
        self.db = self._client[database_name]
        self.col = self.db.users
        self.cache = {}
        
    def new_user(self, id):
        return {
            "id": id,
            "domains": {
                "gplinks.in": True,
                "bit.ly": True,
                "chilp.it": True,
                "click.ru": True,
                "cutt.ly": True,
                "da.gd": True,
                "git.io": True,
                "is.gd": True,
                "osdb.link": True,
                "ow.ly": True,
                "po.st": True,
                "qps.ru": True,
                "short.cm": True,
                "tinyurl.com": True,
                "0x0.st": True,
                "ttm.sh": True
            }
        }
        
    async def add_user(self, id):
        user = self.new_user(id)
        await self.col.insert_one(user)
        
    async def get_user(self, id):
        user = self.cache.get(id)
        if user is not None:
            return user
        
        user = await self.col.find_one({"id": int(id)})
        self.cache[id] = user
        return user
        
    async def is_user_exist(self, id):
        user = await self.col.find_one({'id': int(id)})
        return True if user else False
        
    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count
        
    async def get_all_users(self):
        all_users = self.col.find({})
        return all_users
        
    async def delete_user(self, user_id):
        await self.col.delete_many({'id': int(user_id)})
        
    async def allow_domain(self, id, domain):
        user = await self.get_user(id)
        return user["domains"].get(domain, False)
        
    async def update_domain(self, id, domain, bool):
        user = await self.get_user(id)
        domains = user["domains"]
        self.cache[id]["domains"][domain] = bool 
        domains[domain] = bool
        await self.col.update_one(
            {"id": id},
            {"$set": {"domains": domains}}
        )


BOT_OWNER = int(os.environ.get("BOT_OWNER"))
db = Database()


async def send_msg(user_id, message):
    try:
        await message.copy(chat_id=user_id)
        return 200, None
    except FloodWait as e:
        await asyncio.sleep(e.x)
        return send_msg(user_id, message)
    except InputUserDeactivated:
        return 400, f"{user_id} : deactivated\n"
    except UserIsBlocked:
        return 400, f"{user_id} : blocked the bot\n"
    except PeerIdInvalid:
        return 400, f"{user_id} : user id invalid\n"
    except Exception as e:
        return 500, f"{user_id} : {traceback.format_exc()}\n"


@Client.on_message(filters.private & filters.command("broadcast") & filters.user(BOT_OWNER) & filters.reply, group=10)
async def broadcast(bot, update):
    broadcast_ids = {}
    all_users = await db.get_all_users()
    broadcast_msg = update.reply_to_message
    while True:
        broadcast_id = ''.join([random.choice(string.ascii_letters) for i in range(3)])
        if not broadcast_ids.get(broadcast_id):
            break
    out = await update.reply_text(text=f"Broadcast Started! You will be notified with log file when all the users are notified.")
    start_time = time.time()
    total_users = await db.total_users_count()
    done = 0
    failed = 0
    success = 0
    broadcast_ids[broadcast_id] = dict(total = total_users, current = done, failed = failed, success = success)
    async with aiofiles.open('broadcast.txt', 'w') as broadcast_log_file:
        async for user in all_users:
            sts, msg = await send_msg(user_id = int(user['id']), message = broadcast_msg)
            if msg is not None:
                await broadcast_log_file.write(msg)
            if sts == 200:
                success += 1
            else:
                failed += 1
            if sts == 400:
                await db.delete_user(user['id'])
            done += 1
            if broadcast_ids.get(broadcast_id) is None:
                break
            else:
                broadcast_ids[broadcast_id].update(dict(current = done, failed = failed, success = success))
    if broadcast_ids.get(broadcast_id):
        broadcast_ids.pop(broadcast_id)
    completed_in = datetime.timedelta(seconds=int(time.time()-start_time))
    await asyncio.sleep(3)
    await out.delete()
    if failed == 0:
        await update.reply_text(text=f"broadcast completed in `{completed_in}`\n\nTotal users {total_users}.\nTotal done {done}, {success} success and {failed} failed.", quote=True)
    else:
        await update.reply_document(document='broadcast.txt', caption=f"broadcast completed in `{completed_in}`\n\nTotal users {total_users}.\nTotal done {done}, {success} success and {failed} failed.")
    os.remove('broadcast.txt')
