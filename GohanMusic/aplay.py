# this module i created only for playing music using audio file, idk, because the audio player on play.py module not working so this is the alternative
# audio play function

from os import path

from pyrogram import Client
from pyrogram.types import Message, Voice

from callsmusic import callsmusic, queues

import converter
from downloaders import youtube

from config import BOT_NAME as bn, DURATION_LIMIT, SUPPORT_GROUP, OWNER, BOT_IMAGE as bi
from helpers.filters import command, other_filters
from helpers.decorators import errors
from helpers.errors import DurationLimitError
from helpers.gets import get_url, get_file_name
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


@Client.on_message(command("aplay") & other_filters)
@errors
async def aplay(_, message: Message):

    lel = await message.reply("🔁 **Memproses** audio...")
    sender_id = message.from_user.id
    sender_name = message.from_user.first_name

    keyboard = InlineKeyboardMarkup(
            [
                [
                 InlineKeyboardButton("💬 ɢʀᴏᴜᴘ", url=f"https://t.me/{SUPPORT_GROUP}"),
                 InlineKeyboardButton("ᴏᴡɴᴇʀ 🧑🏻‍💻", url=f"https://t.me/{OWNER}"),
                   
                ]
            ]
        )

    audio = (message.reply_to_message.audio or message.reply_to_message.voice) if message.reply_to_message else None
    url = get_url(message)

    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"❌ Video lebih panjang dari {DURATION_LIMIT} menit tidak diperbolehkan untuk bermain!"
            )

        file_name = get_file_name(audio)
        file_path = await converter.convert(
            (await message.reply_to_message.download(file_name))
            if not path.isfile(path.join("downloads", file_name)) else file_name
        )
    elif url:
        file_path = await converter.convert(youtube.download(url))
    else:
        return await lel.edit_text("❗ Anda tidak memberi saya apa pun untuk dimainkan!")

    if message.chat.id in callsmusic.pytgcalls.active_calls:
        position = await queues.put(message.chat.id, file=file_path)
        await lel.edit(f"#⃣ **Antrian** di posisi {position}!")
    else:
        callsmusic.pytgcalls.join_group_call(message.chat.id, file_path)
        await message.reply_photo(
        photo=f"{bi}",
        reply_markup=keyboard,
        caption="▶️ **Memutar** sebuah lagu oleh {}!".format(
        message.from_user.mention()
        ),
    )
        return await lel.delete()
