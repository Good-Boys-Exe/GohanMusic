from pyrogram import Client, filters
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from config import BOT_NAME, BOT_USERNAME, OWNER, SUPPORT_GROUP
from GohanMusic.msg import Messages as tr
from helpers.filters import command


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
                    InlineKeyboardButton(text="⚔️ ʙᴀɴᴛᴜᴀɴ", callback_data="helps+1"),
                    InlineKeyboardButton(
                        "sᴏᴜᴄʀᴇ 🛠️", url="https://github.com/Good-Boys-Exe/GohanMusic"
                    ),
                ],
            ]
        ),
        disable_web_page_preview=True,
    )


@Client.on_callback_query(filters.regex("cbstart"))
async def cbstart(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""
<b>👋🏻 Hallo {query.message.chat.title}
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
                    InlineKeyboardButton(text="⚔️ ʙᴀɴᴛᴜᴀɴ", callback_data="helps+1"),
                    InlineKeyboardButton(
                        "sᴏᴜᴄʀᴇ 🛠️", url="https://github.com/Good-Boys-Exe/GohanMusic"
                    ),
                ],
            ]
        ),
        disable_web_page_preview=True,
    )


@Client.on_message(command(["help", f"help@{BOT_USERNAME}"]) & ~filters.edited)
async def help(client: Client, message: Message):
    await message.reply_text(
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
                [
                    InlineKeyboardButton(
                        "💬 sᴜᴘᴘᴏʀᴛ", url=f"https://t.me/{SUPPORT_GROUP}"
                    ),
                    InlineKeyboardButton("ᴅᴇᴠᴇʟᴏᴘᴇʀ 🧑🏻‍💻", url=f"https://t.me/{OWNER}"),
                ]
            ]
        ),
    )


help_callback_filter = filters.create(
    lambda _, __, query: query.data.startswith("helps+")
)


@Client.on_callback_query(help_callback_filter)
def helps_answer(client, callback_query):
    chat_id = callback_query.from_user.id
    message_id = callback_query.message.message_id
    msg = int(callback_query.data.split("+")[1])
    client.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=tr.HELPS_MSG[msg],
        reply_markup=InlineKeyboardMarkup(map(msg)),
    )


def map(pos):
    if pos == 1:
        button = [
            [
                InlineKeyboardButton(text="⬅️", callback_data="cbstart"),
                InlineKeyboardButton(text="➡️", callback_data="helps+2"),
            ]
        ]
    elif pos == len(tr.HELPS_MSG) - 1:
        url = f"https://t.me/{SUPPORT_GROUP}"
        button = [
            [
                InlineKeyboardButton(text="⬅️", callback_data=f"helps+{pos-1}"),
                InlineKeyboardButton(text="➡️", callback_data="cbstart"),
            ]
        ]
    else:
        button = [
            [
                InlineKeyboardButton(text="⬅️", callback_data=f"helps+{pos-1}"),
                InlineKeyboardButton(text="➡️", callback_data=f"helps+{pos+1}"),
            ],
        ]
    return button
