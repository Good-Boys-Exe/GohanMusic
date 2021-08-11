import requests
from pyrogram import Client
from config import BOT_USERNAME
from helpers.filters import command

@Client.on_message(command(["truth", f"truth@{BOT_USERNAME}"]))
async def truth(client, message):
    try:
        resp = requests.get("https://tede-api.herokuapp.com/api/truth").json()
        results = f"{resp['message']}"
        return await message.reply_text(results)
    except Exception:
        await message.reply_text("Ada yang salah LOL...")


@Client.on_message(command(["dare", f"dare@{BOT_USERNAME}"]))
async def dare(client, message):
    try:
        resp = requests.get("https://tede-api.herokuapp.com/api/dare").json()
        results = f"{resp['message']}"
        return await message.reply_text(results)
    except Exception:
        await message.reply_text("Ada yang salah LOL...")
