from pyrogram import Client as Bot

from callsmusic import run
from config import API_HASH, API_ID, BOT_TOKEN

bot = Bot(
    ":memory:", API_ID, API_HASH, bot_token=BOT_TOKEN, plugins=dict(root="GohanMusic")
)

bot.start()
run()

