from datetime import datetime
from time import time

from pyrogram import Client, emoji, filters
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from config import BOT_NAME, BOT_USERNAME, OWNER, SUPPORT_GROUP
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


@Client.on_callback_query(filters.regex("close"))
async def close(_, query: CallbackQuery):
    await query.message.delete()


@Client.on_message(
    command(["start", f"start@{BOT_USERNAME}"]) & filters.group & ~filters.edited
)
async def start(client: Client, m: Message):
    current_time = datetime.utcnow()
    start = time()
    m_reply = await m.reply_text(f"{BOT_NAME}")
    delta_ping = time() - start
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await m_reply.edit_text(
        f"""
â **{BOT_NAME}** Online

{emoji.PING_PONG} **PONG!** `{delta_ping * 1000:.3f} ms`

â **Waktu Online:** `{uptime}`

â¨ **Waktu mulai:** `{START_TIME_ISO}`
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("ð§ð»âð» á´á´á´ á´Êá´á´á´Ê", url=f"https://t.me/{OWNER}"),
                    InlineKeyboardButton(
                        "sá´á´á´á´Êá´ ð¬", url=f"https://t.me/{SUPPORT_GROUP}"
                    ),
                ],
                [InlineKeyboardButton("âï¸ Êá´É´á´á´á´É´ âï¸", callback_data="cbghelp")],
            ]
        ),
    )


@Client.on_callback_query(filters.regex("cbgstart"))
async def cbgstart(_, query: CallbackQuery):
    current_time = datetime.utcnow()
    m_reply = await query.message.reply_text(f"{BOT_NAME}")
    await query.message.delete()
    start = time()
    delta_ping = time() - start
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await m_reply.edit_text(
        f"""
â **{BOT_NAME}** Online

{emoji.PING_PONG} **PONG!** `{delta_ping * 1000:.3f} ms`

â **Waktu Online:** `{uptime}`

â¨ **Waktu mulai:** `{START_TIME_ISO}`
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("ð§ð»âð» á´á´á´ á´Êá´á´á´Ê", url=f"https://t.me/{OWNER}"),
                    InlineKeyboardButton(
                        "sá´á´á´á´Êá´ ð¬", url=f"https://t.me/{SUPPORT_GROUP}"
                    ),
                ],
                [InlineKeyboardButton("âï¸ Êá´É´á´á´á´É´ âï¸", callback_data="cbghelp")],
            ]
        ),
    )


@Client.on_message(command("start") & filters.private & ~filters.edited)
async def start_(client: Client, message: Message):
    await message.reply_text(
        f"""
<b>ðð» Hallo {message.from_user.mention}
ðï¸ Nama Saya [{BOT_NAME}](https://t.me/{BOT_USERNAME})

ð¤ Saya Adalah Bot Canggih Yang Dibuat Untuk Memutar Musik Di Obrolan Suara Grup Telegram

âï¸ Klik Tombol Bantuan Untuk Mendapatkan Informasi Cara Menggunaka Bot</b>
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "â á´á´á´Êá´Êá´á´É´ á´á´ É¢Êá´á´á´ â",
                        url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                    )
                ],
                [
                    InlineKeyboardButton(
                        "ð¬ sá´á´á´á´Êá´", url=f"https://t.me/{SUPPORT_GROUP}"
                    ),
                    InlineKeyboardButton("á´á´á´ á´Êá´á´á´Ê ð§ð»âð»", url=f"https://t.me/{OWNER}"),
                ],
                [
                    InlineKeyboardButton("âï¸ Êá´É´á´á´á´É´", callback_data="cbhelp"),
                    InlineKeyboardButton("á´á´É´á´sÉª ð", callback_data="cbdonate"),
                ],
            ]
        ),
        disable_web_page_preview=True,
    )


@Client.on_callback_query(filters.regex("cbstart"))
async def cbstart(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""
<b>ðð» Hallo [{query.message.chat.first_name}](tg://user?id={query.message.chat.id})
ðï¸ Nama Saya [{BOT_NAME}](https://t.me/{BOT_USERNAME})

ð¤ Saya Adalah Bot Canggih Yang Dibuat Untuk Memutar Musik Di Obrolan Suara Grup Telegram

âï¸ Klik Tombol Bantuan Untuk Mendapatkan Informasi Cara Menggunaka Bot</b>
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "â á´á´á´Êá´Êá´á´É´ á´á´ É¢Êá´á´á´ â",
                        url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                    )
                ],
                [
                    InlineKeyboardButton(
                        "ð¬ sá´á´á´á´Êá´", url=f"https://t.me/{SUPPORT_GROUP}"
                    ),
                    InlineKeyboardButton("á´á´á´ á´Êá´á´á´Ê ð§ð»âð»", url=f"https://t.me/{OWNER}"),
                ],
                [
                    InlineKeyboardButton("âï¸ Êá´É´á´á´á´É´", callback_data="cbhelp"),
                    InlineKeyboardButton("á´á´É´á´sÉª ð", callback_data="cbdonate"),
                ],
            ]
        ),
        disable_web_page_preview=True,
    )


@Client.on_callback_query(filters.regex("cbdonate"))
async def donate(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""
<b>â¨ Selamat datang [{query.message.chat.first_name}](tg://user?id={query.message.chat.id})

â¢ Jika berminat berdonasi anda bisa kirim donasi ke pulsa atau ke saldo dana seikhlasnya

â¢ nomer: 089525658633 terimakasih donasimu begitu berarti bagi saya</b>
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="á´á´á´Êá´ÊÉª", callback_data="cbstart")],
            ]
        ),
        disable_web_page_preview=True,
    )


@Client.on_callback_query(filters.regex("cbhelp"))
async def cbhelp(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""
<b>â¨ Selamat datang [{query.message.chat.first_name}](tg://user?id={query.message.chat.id})

Perintah semua anggota grup
â¢ /play (judul lagu)Â - Untuk Memutar lagu yang Anda minta melalui YouTube
â¢ /song (judul lagu) - Untuk Mendownload lagu dari YouTube
â¢ /vsong (judul video) - Untuk Mendownload Video di YouTube
â¢ /search (judul lagu/video)Â - Untuk Mencari link di YouTube dengan detail

Perintah semua admin grup
â¢ /pause - Untuk Menjeda pemutaran Lagu
â¢ /resume - Untuk Melanjutkan pemutaran Lagu yang di pause
â¢ /skip - Untuk Menskip pemutaran lagu ke Lagu berikutnya
â¢ /end - Untuk Memberhentikan pemutaran Lagu
â¢ /reload - Untuk Segarkan daftar admin</b>
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="á´á´á´Êá´ÊÉª", callback_data="cbstart")],
            ]
        ),
        disable_web_page_preview=True,
    )


@Client.on_callback_query(filters.regex("cbghelp"))
async def cbghelp(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""
<b>Perintah semua anggota grup
â¢ /play (judul lagu)Â - Untuk Memutar lagu yang Anda minta melalui YouTube
â¢ /song (judul lagu) - Untuk Mendownload lagu dari YouTube
â¢ /vsong (judul video) - Untuk Mendownload Video di YouTube
â¢ /search (judul lagu/video)Â - Untuk Mencari link di YouTube dengan detail

Perintah semua admin grup
â¢ /pause - Untuk Menjeda pemutaran Lagu
â¢ /resume - Untuk Melanjutkan pemutaran Lagu yang di pause
â¢ /skip - Untuk Menskip pemutaran lagu ke Lagu berikutnya
â¢ /end - Untuk Memberhentikan pemutaran Lagu
â¢ /reload - Untuk Segarkan daftar admin</b>
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="á´á´á´Êá´ÊÉª", callback_data="cbgstart")],
            ]
        ),
        disable_web_page_preview=True,
    )
