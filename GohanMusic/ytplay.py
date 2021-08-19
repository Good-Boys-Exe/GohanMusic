import os
from asyncio.queues import QueueEmpty
from typing import Callable

import aiofiles
import aiohttp
import ffmpeg
import requests
from PIL import Image
from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from Python_ARQ import ARQ
from youtube_search import YoutubeSearch

import converter
from cache.admins import admins as a
from callsmusic import callsmusic, queues
from callsmusic.callsmusic import client as USER
from config import ARQ_API_KEY as arq
from config import BOT_USERNAME, DURATION_LIMIT, SUPPORT_GROUP, que
from downloaders import youtube
from helpers.admins import get_administrators
from helpers.decorators import authorized_users_only
from helpers.filters import command, other_filters

chat_id = None

ARQ_API_KEY = f"{arq}"
aiohttpsession = aiohttp.ClientSession()
arq = ARQ("https://thearq.tech", ARQ_API_KEY, aiohttpsession)


def cb_admin_check(func: Callable) -> Callable:
    async def decorator(client, cb):
        admemes = a.get(cb.message.chat.id)
        if cb.from_user.id in admemes:
            return await func(client, cb)
        await cb.answer("Anda tidak diizinkan!", show_alert=True)
        return

    return decorator


def transcode(filename):
    ffmpeg.input(filename).output(
        "input.raw", format="s16le", acodec="pcm_s16le", ac=2, ar="48k"
    ).overwrite_output().run()
    os.remove(filename)


# Convert seconds to mm:ss
def convert_seconds(seconds):
    seconds = seconds % (24 * 3600)
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d" % (minutes, seconds)


# Convert hh:mm:ss to seconds
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(":"))))


# Change image size
def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage


async def generate_cover(requested_by, title, views, duration, thumbnail):
    async with aiohttp.ClientSession() as session, session.get(thumbnail) as resp:
        if resp.status == 200:
            f = await aiofiles.open("background.png", mode="wb")
            await f.write(await resp.read())
            await f.close()
    image1 = Image.open("./background.png")
    image2 = Image.open("Gohan/ImgPhoto.png")
    image3 = changeImageSize(1280, 720, image1)
    image4 = changeImageSize(1280, 720, image2)
    image5 = image3.convert("RGBA")
    image6 = image4.convert("RGBA")
    Image.alpha_composite(image5, image6).save("temp.png")
    img = Image.open("temp.png")
    img.save("final.png")
    os.remove("temp.png")
    os.remove("background.png")


@Client.on_message(
    command(["playlist", f"playlist@{BOT_USERNAME}"]) & filters.group & ~filters.edited
)
async def playlist(client, message):
    global que
    queue = que.get(message.chat.id)
    if not queue:
        await message.reply_text("**Sedang tidak memutar lagu!**")
    temp = []
    for t in queue:
        temp.append(t)
    now_playing = temp[0][0]
    by = temp[0][1].mention(style="md")
    msg = "**Lagu Yang Sedang dimainkan** di {}".format(message.chat.title)
    msg += "\n• " + now_playing
    msg += "\n• Permintaan " + by
    temp.pop(0)
    if temp:
        msg += "\n\n"
        msg += "**Antrian Lagu**"
        for song in temp:
            name = song[0]
            usr = song[1].mention(style="md")
            msg += f"\n• {name}"
            msg += f"\n• Permintaan {usr}\n"
    await message.reply_text(msg)


# ============================= Settings =========================================
def updated_stats(chat, queue, vol=100):
    if chat.id in callsmusic.pytgcalls.active_calls:
        stats = "Pengaturan dari **{}**".format(chat.title)
        if len(que) > 0:
            stats += "\n\n"
            stats += "Volume: {}%\n".format(vol)
            stats += "Lagu Dalam Antrian: `{}`\n".format(len(que))
            stats += "Sedang Memutar Lagu: **{}**\n".format(queue[0][0])
            stats += "Permintaan: {}".format(queue[0][1].mention)
    else:
        stats = None
    return stats


def r_ply(type_):
    if type_ == "play":
        pass
    else:
        pass
    mar = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("⏹", "leave"),
                InlineKeyboardButton("⏸", "puse"),
                InlineKeyboardButton("▶️", "resume"),
                InlineKeyboardButton("⏭", "skip"),
            ],
            [
                InlineKeyboardButton("📖 ᴘʟᴀʏʟɪsᴛ 📖", "playlist"),
            ],
            [InlineKeyboardButton("🗑️ ᴛᴜᴛᴜᴘ 🗑️", "cls")],
        ]
    )
    return mar


@Client.on_message(
    command(["current", f"current@{BOT_USERNAME}"]) & filters.group & ~filters.edited
)
async def ee(client, message):
    queue = que.get(message.chat.id)
    stats = updated_stats(message.chat, queue)
    if stats:
        await message.reply(stats)
    else:
        await message.reply("**Silahkan Nyalakan dulu VCG nya!**")


@Client.on_message(
    command(["player", f"player@{BOT_USERNAME}"]) & filters.group & ~filters.edited
)
@authorized_users_only
async def settings(client, message):
    playing = None
    if message.chat.id in callsmusic.pytgcalls.active_calls:
        playing = True
    queue = que.get(message.chat.id)
    stats = updated_stats(message.chat, queue)
    if stats:
        if playing:
            await message.reply(stats, reply_markup=r_ply("pause"))

        else:
            await message.reply(stats, reply_markup=r_ply("play"))
    else:
        await message.reply("**Silahkan Nyalakan dulu VCG nya!**")


@Client.on_callback_query(filters.regex(pattern=r"^(playlist)$"))
async def p_cb(b, cb):
    global que
    que.get(cb.message.chat.id)
    type_ = cb.matches[0].group(1)
    cb.message.chat.id
    cb.message.chat
    cb.message.reply_markup.inline_keyboard[1][0].callback_data
    if type_ == "playlist":
        queue = que.get(cb.message.chat.id)
        if not queue:
            await cb.message.edit("**Sedang Tidak Memutar Lagu!**")
        temp = []
        for t in queue:
            temp.append(t)
        now_playing = temp[0][0]
        by = temp[0][1].mention(style="md")
        msg = "**Lagu Yang Sedang Dimainkan** di {}".format(cb.message.chat.title)
        msg += "\n• " + now_playing
        msg += "\n• Permintaan " + by
        temp.pop(0)
        if temp:
            msg += "\n\n"
            msg += "**Antrian Lagu**"
            for song in temp:
                name = song[0]
                usr = song[1].mention(style="md")
                msg += f"\n• {name}"
                msg += f"\n• Permintaan {usr}\n"
        await cb.message.edit(msg)


@Client.on_callback_query(
    filters.regex(pattern=r"^(play|pause|skip|leave|puse|resume|menu|cls)$")
)
@cb_admin_check
async def m_cb(b, cb):
    global que
    qeue = que.get(cb.message.chat.id)
    type_ = cb.matches[0].group(1)
    chat_id = cb.message.chat.id
    m_chat = cb.message.chat

    cb.message.reply_markup.inline_keyboard[1][0].callback_data
    if type_ == "pause":
        if (chat_id not in callsmusic.pytgcalls.active_calls) or (
            callsmusic.pytgcalls.active_calls[chat_id] == "paused"
        ):
            await cb.answer(
                "Assistant Sedang Tidak Terhubung dengan VCG!", show_alert=True
            )
        else:
            callsmusic.pytgcalls.pause_stream(chat_id)

            await cb.answer("Music Paused!")
            await cb.message.edit(
                updated_stats(m_chat, qeue), reply_markup=r_ply("play")
            )

    elif type_ == "play":
        if (chat_id not in callsmusic.pytgcalls.active_calls) or (
            callsmusic.pytgcalls.active_calls[chat_id] == "playing"
        ):
            await cb.answer(
                "Assistant Sedang Tidak Terhubung dengan VCG!", show_alert=True
            )
        else:
            callsmusic.pytgcalls.resume_stream(chat_id)
            await cb.answer("Music Resumed!")
            await cb.message.edit(
                updated_stats(m_chat, qeue), reply_markup=r_ply("pause")
            )

    elif type_ == "playlist":
        queue = que.get(cb.message.chat.id)
        if not queue:
            await cb.message.edit("Sedang Tidak Memutar Lagu")
        temp = []
        for t in queue:
            temp.append(t)
        now_playing = temp[0][0]
        by = temp[0][1].mention(style="md")
        msg = "**Lagu Yang Sedang Dimainkan** di {}".format(cb.message.chat.title)
        msg += "\n• " + now_playing
        msg += "\n• Permintaan " + by
        temp.pop(0)
        if temp:
            msg += "\n\n"
            msg += "**Antrian Lagu**"
            for song in temp:
                name = song[0]
                usr = song[1].mention(style="md")
                msg += f"\n• {name}"
                msg += f"\n• Permintaan {usr}\n"
        await cb.message.edit(msg)

    elif type_ == "resume":
        if (chat_id not in callsmusic.pytgcalls.active_calls) or (
            callsmusic.pytgcalls.active_calls[chat_id] == "playing"
        ):
            await cb.answer(
                "Obrolan tidak terhubung atau sudah dimainkan", show_alert=True
            )
        else:
            callsmusic.pytgcalls.resume_stream(chat_id)
            await cb.answer("Music Resumed!")

    elif type_ == "puse":
        if (chat_id not in callsmusic.pytgcalls.active_calls) or (
            callsmusic.pytgcalls.active_calls[chat_id] == "paused"
        ):
            await cb.answer(
                "Obrolan tidak terhubung atau sudah di pause", show_alert=True
            )
        else:
            callsmusic.pytgcalls.pause_stream(chat_id)

            await cb.answer("Music Paused!")

    elif type_ == "cls":
        await cb.answer("Closed menu")
        await cb.message.delete()

    elif type_ == "menu":
        stats = updated_stats(cb.message.chat, qeue)
        await cb.answer("Menu opened")
        marr = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⏹", "leave"),
                    InlineKeyboardButton("⏸", "puse"),
                    InlineKeyboardButton("▶️", "resume"),
                    InlineKeyboardButton("⏭", "skip"),
                ],
                [
                    InlineKeyboardButton("📖 ᴘʟᴀʏʟɪsᴛ 📖", "playlist"),
                ],
                [InlineKeyboardButton("🗑️ ᴛᴜᴛᴜᴘ 🗑️", "cls")],
            ]
        )
        await cb.message.edit(stats, reply_markup=marr)

    elif type_ == "skip":
        if qeue:
            skip = qeue.pop(0)
        if chat_id not in callsmusic.pytgcalls.active_calls:
            await cb.answer(
                "Assistant Sedang Tidak Terhubung dengan VCG!", show_alert=True
            )
        else:
            callsmusic.queues.task_done(chat_id)

            if callsmusic.queues.is_empty(chat_id):
                callsmusic.pytgcalls.leave_group_call(chat_id)

                await cb.message.edit(
                    "• Tidak Ada Lagi Daftar Putar.\n• Meninggalkan VCG!"
                )
            else:
                callsmusic.pytgcalls.change_stream(
                    chat_id, callsmusic.queues.get(chat_id)["file"]
                )
                await cb.answer("Skipped")
                await cb.message.edit(
                    f"**⏭️ Melewati Lagu:** {skip[0]}\n**▶️ Sekarang Memutar Lagu:** {qeue[0][0]}"
                )

    elif type_ == "leave":
        if chat_id in callsmusic.pytgcalls.active_calls:
            try:
                callsmusic.queues.clear(chat_id)
            except QueueEmpty:
                pass

            callsmusic.pytgcalls.leave_group_call(chat_id)
            await cb.message.edit("**✅ Userbot telah terputus dari obrolan suara.**")
        else:
            await cb.answer(
                "Assistant Sedang Tidak Terhubung dengan VCG!", show_alert=True
            )


@Client.on_message(command(["ytplay", f"ytplay@{BOT_USERNAME}"]) & other_filters)
async def play(_, message: Message):
    global que
    lel = await message.reply("**🔎 Sedang Mencari Lagu**")
    administrators = await get_administrators(message.chat)
    chid = message.chat.id
    try:
        user = await USER.get_me()
    except:
        user.first_name = "helper"
    usar = user
    wew = usar.id
    try:
        await _.get_chat_member(chid, wew)
    except:
        for administrator in administrators:
            if administrator == message.from_user.id:
                try:
                    invitelink = await _.export_chat_invite_link(chid)
                except:
                    await lel.edit(
                        "<b>Tambahkan saya sebagai admin group Anda terlebih dahulu.</b>",
                    )
                    return

                try:
                    await USER.join_chat(invitelink)
                    await USER.send_message(
                        message.chat.id,
                        "Saya bergabung dengan group ini untuk memainkan musik di VCG.",
                    )
                    await lel.edit(
                        "<b>{user.first_name} berhasil bergabung dengan Group anda</b>",
                    )

                except UserAlreadyParticipant:
                    pass
                except Exception:
                    await lel.edit(
                        f"<b>🔴 Flood Wait Error 🔴 \n{user.first_name} tidak dapat bergabung dengan group Anda karena banyaknya permintaan bergabung untuk assistant! Pastikan assistan tidak dibanned didalam grup."
                        f"\n\nAtau tambahkan @{user.username} Bot secara manual ke Group Anda dan coba lagi.</b>",
                    )
    try:
        await USER.get_chat(chid)
    except:
        await lel.edit(
            f"<b>{user.first_name}\nterkena banned dari Group ini, Minta admin untuk kirim perintah `/unban @{user.username}` di grup ini kemudian kirim perintah `/userbotjoin` di grup ini untuk mengundang assistant ke dalam grup anda</b>"
        )
        return
    message.from_user.id
    message.from_user.first_name
    message.from_user.id
    user_id = message.from_user.id
    message.from_user.first_name
    user_name = message.from_user.first_name
    rpk = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"

    query = ""
    for i in message.command[1:]:
        query += " " + str(i)
    print(query)
    await lel.edit("**🔄 Sedang Memproses Lagu**")
    ydl_opts = {
        "format": "bestaudio/best",
    }
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        url = f"https://www.youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:250]
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f"thumb{title}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
        duration = results[0]["duration"]
        results[0]["url_suffix"]
        views = results[0]["views"]

    except Exception as e:
        await lel.edit(
            "**❌ Lagu tidak ditemukan ❌**\nCoba masukan judul lagu yang lebih jelas"
        )
        print(str(e))
        return
    try:
        secmul, dur, dur_arr = 1, 0, duration.split(":")
        for i in range(len(dur_arr) - 1, -1, -1):
            dur += int(dur_arr[i]) * secmul
            secmul *= 60
        if (dur / 60) > DURATION_LIMIT:
            await lel.edit(
                f"**❌ Lagu dengan durasi lebih dari `{DURATION_LIMIT}` menit tidak dapat diputar!\n🎧 Lagu yang di minta berdurasi `{duration}` menit**"
            )
            return
    except:
        pass
    durl = url
    durl = durl.replace("youtube", "youtubepp")
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("⏯ ᴍᴇɴᴜ", callback_data="menu"),
                InlineKeyboardButton("ᴛᴜᴛᴜᴘ 🗑", callback_data="cls"),
            ],
            [
                InlineKeyboardButton(
                    "💬 sᴜᴘᴘᴏʀᴛ ᴄʜᴀᴛ 💬", url=f"https://t.me/{SUPPORT_GROUP}"
                )
            ],
        ]
    )
    requested_by = message.from_user.first_name
    await generate_cover(requested_by, title, views, duration, thumbnail)
    file_path = await converter.convert(youtube.download(url))

    if message.chat.id in callsmusic.pytgcalls.active_calls:
        position = await queues.put(message.chat.id, file=file_path)
        qeue = que.get(message.chat.id)
        s_name = title
        r_by = message.from_user
        loc = file_path
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)
        await message.reply_photo(
            photo="final.png",
            caption=f"🏷 **Judul:** [{title}]({url})\n⏱ **Durasi:** `{duration}`\n💡 **Status:** `Antrian ke {position}`\n"
            + f"🎧 **Permintaan** {message.from_user.mention}",
            reply_markup=keyboard,
        )
        os.remove("final.png")
        return await lel.delete()
    chat_id = message.chat.id
    que[chat_id] = []
    qeue = que.get(message.chat.id)
    s_name = title
    r_by = message.from_user
    loc = file_path
    appendable = [s_name, r_by, loc]
    qeue.append(appendable)
    callsmusic.pytgcalls.join_group_call(message.chat.id, file_path)
    await message.reply_photo(
        photo="final.png",
        caption=f"🏷 **Judul:** [{title}]({url})\n⏱ **Durasi:** `{duration}`\n💡 **Status:** `Memutar`\n"
        + f"🎧 **Permintaan:** {message.from_user.mention}",
        reply_markup=keyboard,
    )
    os.remove("final.png")
    return await lel.delete()
