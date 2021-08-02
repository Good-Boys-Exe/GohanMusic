from time import time
from datetime import datetime
from config import BOT_USERNAME, BOT_NAME, ASSISTANT_NAME, SUPPORT_GROUP, START_IMAGE, OWNER
from helpers.filters import command
from pyrogram import Client, filters, emoji
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from helpers.decorators import authorized_users_only


@Client.on_message(command("start") & filters.private & ~filters.edited)
async def start_(client: Client, message: Message):
    await message.reply_photo(
       photo = f"{START_IMAGE}",
       caption = f"""<b>👋🏻 Hallo {message.from_user.mention}
🎟️ Nama Saya Adalah [{BOT_NAME}](https://t.me/{BOT_USERNAME})

🤖 Saya Adalah Bot Canggih Yang Dibuat Untuk Memutar Musik Di Obrolan Suara Grup Telegram

✏️ Tekan » /help « Untuk Melihat Daftar Perintah Yang Saya Punya</b>""",
        reply_markup=InlineKeyboardMarkup(
            [ 
                [
                    InlineKeyboardButton(
                        "➕ ᴛᴀᴍʙᴀʜᴋᴀɴ ᴋᴇ ɢʀᴏᴜᴘ ➕", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
                  ],[
                    InlineKeyboardButton(
                         "🙎🏻‍♂ ᴀssɪsᴛᴀɴᴛ", url=f"https://t.me/{ASSISTANT_NAME}"),
                    InlineKeyboardButton(
                        "ᴅᴇᴠᴇʟᴏᴘᴇʀ 🧑🏻‍💻", url=f"https://t.me/{OWNER}")
                  ],[
                    InlineKeyboardButton(
                         "✨ sᴏᴜʀᴄᴇ ᴄᴏᴅᴇ ✨", url="https://github.com/Good-Boys-Exe/GohanMusic")
                ]
            ]
        )
    )


@Client.on_message(command("help") & filters.private & ~filters.edited)
async def help(client: Client, message: Message):
    await message.reply_photo(
       photo = f"{START_IMAGE}",
       caption = f"""<b>Hallo {message.from_user.mention}
\nPerintah semua anggota grup:
/play (judul lagu) - Untuk Memutar lagu yang Anda minta melalui YouTube
/playlist - Untuk Menampilkan daftar putar Lagu sekarang
/current - Untuk Menunjukkan  Lagu sekarang yang sedang diputar
/song (judul lagu) - Untuk Mendownload lagu dari YouTube 
/search (judul lagu/video) - Untuk Mencari link di YouTube dengan detail
/video (judul video) - Untuk Mendownload Video di YouTube

\nPerintah semua admin grup:
/player - Buka panel pengaturan pemutar musik
/pause - Untuk Menjeda pemutaran Lagu
/resume - Untuk Melanjutkan pemutaran Lagu yang di pause
/skip - Untuk Menskip pemutaran lagu ke Lagu berikutnya
/end - Untuk Memberhentikan pemutaran Lagu
/userbotjoin - Untuk Mengundang asisten ke obrolan Anda
/reload - Untuk Segarkan daftar admin
</b>""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "💬 sᴜᴘᴘᴏʀᴛ", url=f"https://t.me/{SUPPORT_GROUP}"),
                    InlineKeyboardButton(
                        "ᴅᴇᴠᴇʟᴏᴘᴇʀ 🧑🏻‍💻", url=f"https://t.me/{OWNER}")
                ]
            ]
        )
    )


@Client.on_message(command(["help", f"help@{BOT_USERNAME}"]) & ~filters.edited)
async def help(client: Client, message: Message):
    await message.reply_photo(
       photo = f"{START_IMAGE}",
       caption = f"""<b>Hallo {message.from_user.mention}
\nPerintah semua anggota grup:
/play (judul lagu) - Untuk Memutar lagu yang Anda minta melalui YouTube
/playlist - Untuk Menampilkan daftar putar Lagu sekarang
/current - Untuk Menunjukkan  Lagu sekarang yang sedang diputar
/song (judul lagu) - Untuk Mendownload lagu dari YouTube 
/search (judul lagu/video) - Untuk Mencari link di YouTube dengan detail
/video (judul video) - Untuk Mendownload Video di YouTube dengan detail
\nPerintah semua admin grup:
/player - Buka panel pengaturan pemutar musik
/pause - Untuk Menjeda pemutaran Lagu
/resume - Untuk Melanjutkan pemutaran Lagu yang di pause
/skip - Untuk Menskip pemutaran lagu ke Lagu berikutnya
/end - Untuk Memberhentikan pemutaran Lagu
/userbotjoin - Untuk Mengundang asisten ke obrolan Anda
/reload - Untuk Segarkan daftar admin
</b>""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "💬 sᴜᴘᴘᴏʀᴛ", url=f"https://t.me/{SUPPORT_GROUP}"),
                    InlineKeyboardButton(
                        "ᴅᴇᴠᴇʟᴏᴘᴇʀ 🧑🏻‍💻", url=f"https://t.me/{OWNER}")
                ]
            ]
        )
    )


