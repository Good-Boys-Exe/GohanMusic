from datetime import datetime

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
async def start(client: Client, message: Message):
    current_time = datetime.utcnow()
    delta_ping = time() - start
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await message.reply_text(
        f"""
✅ **{BOT_NAME}** Online

{emoji.PING_PONG} **PONG!** `{delta_ping * 1000:.3f}`

⌚ **Waktu Online:** `{uptime}`

✨ **Waktu mulai:** `{START_TIME_ISO}`
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🧑🏻‍💻 ᴅᴇᴠᴇʟᴏᴘᴇʀ", url=f"https://t.me/{OWNER}"),
                    InlineKeyboardButton(
                        "sᴜᴘᴘᴏʀᴛ 💬", url=f"https://t.me/{SUPPORT_GROUP}"
                    ),
                ],
                [InlineKeyboardButton("⚔️ ʙᴀɴᴛᴜᴀɴ ⚔️", callback_data="cbghelp")],
            ]
        ),
    )


@Client.on_callback_query(filters.regex("cbgstart"))
async def cbstart(_, query: CallbackQuery):
    current_time = datetime.utcnow()
    delta_ping = time() - start
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await query.edit_message_text(
        f"""
✅ **{BOT_NAME}** Online

{emoji.PING_PONG} **PONG!** `{delta_ping * 1000:.3f}`

⌚ **Waktu Online:** `{uptime}`

✨ **Waktu mulai:** `{START_TIME_ISO}`
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="ᴋᴇᴍʙᴀʟɪ", callback_data="cbgstart")],
            ]
        ),
        disable_web_page_preview=True,
    )


@Client.on_message(command("start") & filters.private & ~filters.edited)
async def start_(client: Client, message: Message):
    await message.reply_text(
        f"""
<b>👋🏻 Hallo {message.from_user.mention}
🎟️ Nama Saya [{BOT_NAME}](https://t.me/{BOT_USERNAME})

🤖 Saya Adalah Bot Canggih Yang Dibuat Untuk Memutar Musik Di Obrolan Suara Grup Telegram

⚔️ Klik Tombol Bantuan Untuk Mendapatkan Informasi Cara Menggunaka Bot</b>
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "➕ ᴛᴀᴍʙᴀʜᴋᴀɴ ᴋᴇ ɢʀᴏᴜᴘ ➕",
                        url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                    )
                ],
                [
                    InlineKeyboardButton(
                        "💬 sᴜᴘᴘᴏʀᴛ", url=f"https://t.me/{SUPPORT_GROUP}"
                    ),
                    InlineKeyboardButton("ᴅᴇᴠᴇʟᴏᴘᴇʀ 🧑🏻‍💻", url=f"https://t.me/{OWNER}"),
                ],
                [
                    InlineKeyboardButton("⚔️ ʙᴀɴᴛᴜᴀɴ", callback_data="cbhelp"),
                    InlineKeyboardButton("ᴅᴏɴᴀsɪ 🎁", callback_data="cbdonate"),
                ],
            ]
        ),
        disable_web_page_preview=True,
    )


@Client.on_callback_query(filters.regex("cbstart"))
async def cbstart(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""
<b>👋🏻 Hallo [{query.message.chat.first_name}](tg://user?id={query.message.chat.id})
🎟️ Nama Saya [{BOT_NAME}](https://t.me/{BOT_USERNAME})

🤖 Saya Adalah Bot Canggih Yang Dibuat Untuk Memutar Musik Di Obrolan Suara Grup Telegram

⚔️ Klik Tombol Bantuan Untuk Mendapatkan Informasi Cara Menggunaka Bot</b>
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "➕ ᴛᴀᴍʙᴀʜᴋᴀɴ ᴋᴇ ɢʀᴏᴜᴘ ➕",
                        url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                    )
                ],
                [
                    InlineKeyboardButton(
                        "💬 sᴜᴘᴘᴏʀᴛ", url=f"https://t.me/{SUPPORT_GROUP}"
                    ),
                    InlineKeyboardButton("ᴅᴇᴠᴇʟᴏᴘᴇʀ 🧑🏻‍💻", url=f"https://t.me/{OWNER}"),
                ],
                [
                    InlineKeyboardButton("⚔️ ʙᴀɴᴛᴜᴀɴ", callback_data="cbhelp"),
                    InlineKeyboardButton("ᴅᴏɴᴀsɪ 🎁", callback_data="cbdonate"),
                ],
            ]
        ),
        disable_web_page_preview=True,
    )


@Client.on_callback_query(filters.regex("cbdonate"))
async def donate(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""
<b>✨ Selamat datang [{query.message.chat.first_name}](tg://user?id={query.message.chat.id})

• Jika berminat berdonasi anda bisa kirim donasi ke pulsa atau ke saldo dana seikhlasnya

• nomer: 089525658633 terimakasih donasimu begitu berarti bagi saya</b>
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="ᴋᴇᴍʙᴀʟɪ", callback_data="cbstart")],
            ]
        ),
        disable_web_page_preview=True,
    )


@Client.on_callback_query(filters.regex("cbhelp"))
async def cbhelp(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""
<b>Perintah semua anggota grup
• /play (judul lagu) - Untuk Memutar lagu yang Anda minta melalui YouTube
• /song (judul lagu) - Untuk Mendownload lagu dari YouTube
• /vsong (judul video) - Untuk Mendownload Video di YouTube
• /search (judul lagu/video) - Untuk Mencari link di YouTube dengan detail

Perintah semua admin grup
• /pause - Untuk Menjeda pemutaran Lagu
• /resume - Untuk Melanjutkan pemutaran Lagu yang di pause
• /skip - Untuk Menskip pemutaran lagu ke Lagu berikutnya
• /end - Untuk Memberhentikan pemutaran Lagu
• /reload - Untuk Segarkan daftar admin</b>
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="ᴋᴇᴍʙᴀʟɪ", callback_data="cbstart")],
            ]
        ),
        disable_web_page_preview=True,
    )


@Client.on_callback_query(filters.regex("cbghelp"))
async def cbghelp(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""
<b>Perintah semua anggota grup
• /play (judul lagu) - Untuk Memutar lagu yang Anda minta melalui YouTube
• /song (judul lagu) - Untuk Mendownload lagu dari YouTube
• /vsong (judul video) - Untuk Mendownload Video di YouTube
• /search (judul lagu/video) - Untuk Mencari link di YouTube dengan detail

Perintah semua admin grup
• /pause - Untuk Menjeda pemutaran Lagu
• /resume - Untuk Melanjutkan pemutaran Lagu yang di pause
• /skip - Untuk Menskip pemutaran lagu ke Lagu berikutnya
• /end - Untuk Memberhentikan pemutaran Lagu
• /reload - Untuk Segarkan daftar admin</b>
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="ᴋᴇᴍʙᴀʟɪ", callback_data="cbgstart")],
            ]
        ),
        disable_web_page_preview=True,
    )
