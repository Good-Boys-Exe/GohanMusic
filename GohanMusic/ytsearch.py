import logging

from pyrogram import Client
from pyrogram.types import Message
from youtube_search import YoutubeSearch

from config import BOT_USERNAME
from helpers.filters import command

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


logging.getLogger("pyrogram").setLevel(logging.WARNING)


@Client.on_message(command(["search", f"search@{BOT_USERNAME}"]))
async def ytsearch(_, message: Message):
    try:
        if len(message.command) < 2:
            await message.reply_text("**/search masukan judul video!**")
            return
        query = message.text.split(None, 1)[1]
        m = await message.reply_text("🔎 **Sedang Mencari Video**")
        results = YoutubeSearch(query, max_results=5).to_dict()
        i = 0
        text = ""
        while i < 5:
            text += f"**Judul:** `{results[i]['title']}`\n"
            text += f"**Durasi:** {results[i]['duration']}\n"
            text += f"**Penonton:** {results[i]['views']}\n"
            text += f"**Channel:** {results[i]['channel']}\n"
            text += f"https://www.youtube.com{results[i]['url_suffix']}\n\n"
            i += 1
        await m.edit(text, disable_web_page_preview=True)
    except Exception as e:
        await message.reply_text(str(e))

