from datetime import datetime
from time import time

from pyrogram import Client, emoji, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from config import BOT_NAME as bn
from config import BOT_USERNAME, OWNER, SUPPORT_GROUP
from helpers.decorators import authorized_users_only
from helpers.filters import command

START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ("Minggu", 60 * 60 * 24 * 7),
    ("Hari", 60 * 60 * 24),
    ("Jam", 60 * 60),
    ("Menit", 60),
    ("Detik", 1),
)


async def _human_time_duration(seconds):
    if seconds == 0:
        return "inf"
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append("{} {}{}".format(amount, unit, "" if amount == 1 else ""))
    return ", ".join(parts)


@Client.on_message(
    command(["start", f"start@{BOT_USERNAME}"]) & filters.group & ~filters.edited
)
async def start(client: Client, message: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await message.reply_text(
        f"""✅ **{bn}** Sedang Online!\n<b>Waktu Online:</b> `{uptime}`""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🧑🏻‍💻 ᴅᴇᴠᴇʟᴏᴘᴇʀ", url=f"https://t.me/{OWNER}"),
                    InlineKeyboardButton(
                        "sᴜᴘᴘᴏʀᴛ 💬", url=f"https://t.me/{SUPPORT_GROUP}"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "🛠 sᴏᴜʀᴄᴇ ᴄᴏᴅᴇ 🛠",
                        url="https://github.com/Good-Boys-Exe/GohanMusic",
                    )
                ],
            ]
        ),
    )


@Client.on_message(command(["ping", f"ping@{BOT_USERNAME}"]) & ~filters.edited)
async def ping_pong(client: Client, m: Message):
    start = time()
    m_reply = await m.reply_text("Pinging...")
    delta_ping = time() - start
    await m_reply.edit_text(
        f"{emoji.PING_PONG} **PONG!!**\n" f"`{delta_ping * 1000:.3f} ms`"
    )


@Client.on_message(command(["uptime", f"uptime@{BOT_USERNAME}"]) & ~filters.edited)
@authorized_users_only
async def get_uptime(client: Client, m: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await m.reply_text(
        f"{emoji.ROBOT} Status\n"
        f"• **Waktu aktif:** `{uptime}`\n"
        f"• **Waktu mulai:** `{START_TIME_ISO}`"
    )
