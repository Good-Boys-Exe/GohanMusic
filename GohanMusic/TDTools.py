# 🍀 © @tofik_dn
# ⚠️ Do not remove credits

import requests
from pyrogram import Client
from config import BOT_USERNAME as bu, OWNER as o
from helpers.filters import command


@Client.on_message(command(["asupan", f"asupan@{bu}"]))
async def asupan(client, message):
    try:
        resp = requests.get("https://tede-api.herokuapp.com/api/asupan/ptl").json()
        results = f"{resp['url']}"
        return await client.send_video(message.chat.id, video=results, caption=f"@{o}")
    except Exception:
        await message.reply_text("Ada yang salah LOL...")


@Client.on_message(command(["wibu", f"wibu@{bu}"]))
async def wibu(client, message):
    try:
        resp = requests.get("https://tede-api.herokuapp.com/api/asupan/wibu").json()
        results = f"{resp['url']}"
        return await client.send_video(message.chat.id, video=results, caption=f"@{o}")
    except Exception:
        await message.reply_text("Ada yang salah LOL...")


@Client.on_message(command(["chika", f"chika@{bu}"]))
async def chika(client, message):
    try:
        resp = requests.get("https://tede-api.herokuapp.com/api/chika").json()
        results = f"{resp['url']}"
        return await client.send_video(message.chat.id, video=results, caption=f"@{o}")
    except Exception:
        await message.reply_text("Ada yang salah LOL...")


@Client.on_message(command(["truth", f"truth@{bu}"]))
async def truth(client, message):
    try:
        resp = requests.get("https://tede-api.herokuapp.com/api/truth").json()
        results = f"{resp['message']}"
        return await message.reply_text(results)
    except Exception:
        await message.reply_text("Ada yang salah LOL...")


@Client.on_message(command(["dare", f"dare@{bu}"]))
async def dare(client, message):
    try:
        resp = requests.get("https://tede-api.herokuapp.com/api/dare").json()
        results = f"{resp['message']}"
        return await message.reply_text(results)
    except Exception:
        await message.reply_text("Ada yang salah LOL...")


@Client.on_message(command(["lyric", f"lyric@{bu}"]))
async def lirik(_, message):
    try:
        if len(message.command) < 2:
            await message.reply_text("**Nyari apa?**")
            return
        query = message.text.split(None, 1)[1]
        rep = await message.reply_text("🔎 **Sedang Mencari lyrics**")
        resp = requests.get(f"https://tede-api.herokuapp.com/api/lirik?l={query}").json()
        result = f"{resp['data']}"
        await rep.edit(result)
    except Exception:
        await rep.edit("**Lyrics tidak ditemukan.** Coba cari dengan judul lagu yang lebih jelas")
