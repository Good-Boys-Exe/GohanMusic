# 🍀 © @tofik_dn
# ⚠️ Do not remove credits

import requests
from config import BOT_USERNAME
from pyrogram import Client
from helpers.filters import command


@Client.on_message(command(["lyric", f"lyric@{BOT_USERNAME}"]))
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
