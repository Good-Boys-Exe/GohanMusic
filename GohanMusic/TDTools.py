# 🍀 © @tofik_dn
# ⚠️ Do not remove credits

import requests
from pyrogram import Client

from callsmusic.callsmusic import client as USER
from config import BOT_USERNAME as bu
from helpers.filters import command


@Client.on_message(command(["asupan", f"asupan@{bu}"]))
async def asupan(client, message):
    message.from_user.id
    message.from_user.first_name
    user_id = message.from_user.id
    message.from_user.first_name
    user_name = message.from_user.first_name
    rpk = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
    try:
        resp = requests.get("https://api-tede.herokuapp.com/api/asupan/ptl").json()
        results = f"{resp['url']}"
        return await client.send_video(
            message.chat.id, video=results, caption=f"{rpk} biar nggak ngantuk"
        )
    except Exception:
        await message.reply_text("Ada yang salah LOL...")


@Client.on_message(command(["wibu", f"wibu@{bu}"]))
async def wibu(client, message):
    message.from_user.id
    message.from_user.first_name
    user_id = message.from_user.id
    message.from_user.first_name
    user_name = message.from_user.first_name
    rpk = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
    try:
        resp = requests.get("https://api-tede.herokuapp.com/api/asupan/wibu").json()
        results = f"{resp['url']}"
        return await client.send_video(
            message.chat.id, video=results, caption=f"{rpk} wibu ternyata!"
        )
    except Exception:
        await message.reply_text("Ada yang salah LOL...")


@Client.on_message(command(["chika", f"chika@{bu}"]))
async def chika(client, message):
    message.from_user.id
    message.from_user.first_name
    user_id = message.from_user.id
    message.from_user.first_name
    user_name = message.from_user.first_name
    rpk = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
    try:
        resp = requests.get("https://api-tede.herokuapp.com/api/chika").json()
        results = f"{resp['url']}"
        return await client.send_video(
            message.chat.id, video=results, caption=f"{rpk} cantik nggak?"
        )
    except Exception:
        await message.reply_text("Ada yang salah LOL...")


@Client.on_message(command(["truth", f"truth@{bu}"]))
async def truth(client, message):
    message.from_user.id
    message.from_user.first_name
    user_id = message.from_user.id
    message.from_user.first_name
    user_name = message.from_user.first_name
    rpk = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
    try:
        resp = requests.get("https://api-tede.herokuapp.com/api/truth").json()
        results = f"{rpk} {resp['message']}"
        return await message.reply_text(results)
    except Exception:
        await message.reply_text("Ada yang salah LOL...")


@Client.on_message(command(["dare", f"dare@{bu}"]))
async def dare(client, message):
    message.from_user.id
    message.from_user.first_name
    user_id = message.from_user.id
    message.from_user.first_name
    user_name = message.from_user.first_name
    rpk = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
    try:
        resp = requests.get("https://api-tede.herokuapp.com/api/dare").json()
        results = f"{rpk} {resp['message']}"
        return await message.reply_text(results)
    except Exception:
        await message.reply_text("Ada yang salah LOL...")


@Client.on_message(command(["lyrics", f"lyrics@{bu}"]))
async def lirik(_, message):
    message.from_user.id
    message.from_user.first_name
    user_id = message.from_user.id
    message.from_user.first_name
    user_name = message.from_user.first_name
    rpk = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
    try:
        if len(message.command) < 2:
            await message.reply_text("**Nyari apa?**")
            return
        query = message.text.split(None, 1)[1]
        rep = await message.reply_text(f"🔎 **Lirik sedang dicari {rpk}**")
        resp = requests.get(
            f"https://api-tede.herokuapp.com/api/lirik?l={query}"
        ).json()
        result = f"{resp['data']}"
        await rep.edit(result)
    except Exception:
        await rep.edit(
            f"**Lyrics tidak ditemukan.** {rpk} \nCoba cari dengan judul lagu yang lebih jelas"
        )


@Client.on_message(command(["songs", f"songs@{bu}"]))
async def songs(client, message):
    message.from_user.id
    message.from_user.first_name
    user_id = message.from_user.id
    message.from_user.first_name
    user_name = message.from_user.first_name
    rpk = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
    try:
        if len(message.command) < 2:
            await message.reply_text(
                f"❌ **Lagu Tidak ditemukan.** {rpk}\n\n**Coba Masukan Judul lagu yang lebih jelas.**"
            )
            return
        text = message.text.split(None, 1)[1]
        results = await USER.get_inline_bot_results(473587803, f"{text}")
        await USER.send_inline_bot_result(
            message.chat.id, results.query_id, results.results[0].id
        )
    except Exception:
        await message.reply_text(f"❌ **Lagu Tidak ditemukan** {rpk}")
