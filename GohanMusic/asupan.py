# 🍀 © @tofik_dn
# ⚠️ Do not remove credits

import requests
from pyrogram import Client
from config import BOT_USERNAME as bu
from helpers.filters import command

@Client.on_message(command(["asupan", f"asupan@{bu}"]))
async def asupan(client, message):
    try:
        resp = requests.get("https://tede-api.herokuapp.com/api/asupan/ptl").json()
        results = f"{resp['url']}"
        return await client.send_video(message.chat.id, video=results, caption=f"{resp['by']}")
    except Exception:
        await message.reply_text("`Something went wrong LOL...`")


@Client.on_message(command(["wibu", f"wibu@{bu}"]))
async def wibu(client, message):
    try:
        resp = requests.get("https://tede-api.herokuapp.com/api/asupan/wibu").json()
        results = f"{resp['url']}"
        return await client.send_video(message.chat.id, video=results, caption=f"{resp['by']}")
    except Exception:
        await message.reply_text("`Something went wrong LOL...`")


@Client.on_message(command(["chika", f"chika@{bu}"]))
async def chika(client, message):
    try:
        resp = requests.get("https://tede-api.herokuapp.com/api/chika").json()
        results = f"{resp['url']}"
        return await client.send_video(message.chat.id, video=results, caption=f"{resp['by']}")
    except Exception:
        await message.reply_text("`Something went wrong LOL...`")
