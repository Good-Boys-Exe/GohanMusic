import io
import os
import random
from asyncio.queues import QueueEmpty
from typing import Callable

import aiofiles
import aiohttp
import ffmpeg
import requests
from PIL import Image, ImageDraw, ImageFont
from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from Python_ARQ import ARQ
from youtube_search import YoutubeSearch

import converter
from cache.admins import admins as a
from callsmusic import callsmusic, queues
from callsmusic.callsmusic import client as USER
from config import ARQ_API_KEY as aak
from config import BOT_NAME as bn
from config import BOT_USERNAME as bu
from config import DURATION_LIMIT, SUPPORT_GROUP, que
from converter.converter import path
from downloaders import youtube
from helpers.admins import get_administrators
from helpers.channelmusic import get_chat_id
from helpers.decorators import authorized_users_only, errors
from helpers.filters import command, other_filters
from helpers.gets import get_file_name, get_url

ARQ_API_KEY = f"{aak}"
aiohttpsession = aiohttp.ClientSession()
arq = ARQ("https://thearq.tech", ARQ_API_KEY, aiohttpsession)


GOHAN_IMG = [
    "https://telegra.ph/file/159431ea489ecc68f19f0.png",
    "https://telegra.ph/file/1588cb26e8c79a80d6c32.png",
    "https://telegra.ph/file/9fb646ad170d0512aa447.png",
    "https://telegra.ph/file/c03210961ae494a616542.png",
    "https://telegra.ph/file/07db27b4941d88d200121.png",
    "https://telegra.ph/file/6d88487537ed16d78f7bf.png"
]


def cb_admin_check(func: Callable) -> Callable:
    async def decorator(client, cb):
        admemes = a.get(cb.message.chat.id)
        if cb.from_user.id in admemes:
            return await func(client, cb)
        await cb.answer("Anda Bukan Admin Dari Grup Ini!", show_alert=True)
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
    PNG = Image.open("./background.png")
    GOHAN_THUMBNAIL = random.choice(GOHAN_IMG)
    AMBIL_FOTO = Image.open(io.BytesIO(requests.get(GOHAN_THUMBNAIL).content))
    IMAGE1 = changeImageSize(1280, 720, PNG)
    IMAGE2 = changeImageSize(1280, 720, AMBIL_FOTO)
    IMAGE3 = IMAGE1.convert("RGBA")
    IMAGE4 = IMAGE2.convert("RGBA")
    Image.alpha_composite(IMAGE3, IMAGE4).save("temp.png")
    img = Image.open("temp.png")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("etc/Roboto-Medium.ttf", 60)
    font2 = ImageFont.truetype("etc/finalfont.ttf", 70)
    draw.text((25, 550), f"Diputar di: {requested_by[:15]}...", (0, 0, 0), font=font)
    draw.text((25, 630), f"{title[:25]}...", (0, 0, 0), font=font2)
    img.save("final.png")
    os.remove("temp.png")
    os.remove("background.png")


@Client.on_message(
    command(["playlist", f"playlist@{bu}"]) & filters.group & ~filters.edited
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
        await message.reply_text(
            msg,
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("⏯ ᴍᴇɴᴜ ᴘᴇᴍᴜᴛᴀʀᴀɴ ⏯", callback_data="menu")],
                    [
                        InlineKeyboardButton(
                            "💬 sᴜᴘᴘᴏʀᴛ ᴄʜᴀᴛ 💬", url=f"https://t.me/{SUPPORT_GROUP}"
                        )
                    ],
                ]
            ),
        )


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
                InlineKeyboardButton("▶️", "resume"),
                InlineKeyboardButton("⏸️", "puse"),
                InlineKeyboardButton("⏭️", "skip"),
                InlineKeyboardButton("⏹️", "leave"),
            ],
            [InlineKeyboardButton("📖 ᴅᴀғᴛᴀʀ ᴘᴜᴛᴀʀ 📖", callback_data="playlist")],
            [InlineKeyboardButton("🗑️ ᴛᴜᴛᴜᴘ ᴍᴇɴᴜ 🗑️", callback_data="close")],
        ]
    )
    return mar


@Client.on_message(
    command(["player", f"player@{bu}"]) & filters.group & ~filters.edited
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
        await cb.message.edit(
            msg,
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("⏯ ᴍᴇɴᴜ ᴘᴇᴍᴜᴛᴀʀᴀɴ ⏯", callback_data="menu")],
                    [
                        InlineKeyboardButton(
                            "💬 sᴜᴘᴘᴏʀᴛ ᴄʜᴀᴛ 💬", url=f"https://t.me/{SUPPORT_GROUP}"
                        )
                    ],
                ]
            ),
        )


@Client.on_callback_query(
    filters.regex(pattern=r"^(play|playlist|pause|skip|leave|puse|resume|menu|cls)$")
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
                    InlineKeyboardButton("▶️", "resume"),
                    InlineKeyboardButton("⏸️", "puse"),
                    InlineKeyboardButton("⏭️", "skip"),
                    InlineKeyboardButton("⏹️", "leave"),
                ],
                [InlineKeyboardButton("📖 ᴅᴀғᴛᴀʀ ᴘᴜᴛᴀʀ 📖", callback_data="playlist")],
                [InlineKeyboardButton("🗑️ ᴛᴜᴛᴜᴘ ᴍᴇɴᴜ 🗑️", callback_data="close")],
            ]
        )
        await cb.message.edit(stats, reply_markup=marr)

    elif type_ == "skip":
        if qeue:
            qeue.pop(0)
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


@Client.on_message(command(["play", f"play@{bu}"]) & other_filters)
@errors
async def play(_, message: Message):
    global que
    lel = await message.reply("**🔎 Pencarian**")
    administrators = await get_administrators(message.chat)
    chid = message.chat.id
    try:
        user = await USER.get_me()
    except:
        user.first_name = "helper"
    usar = user
    wew = usar.id
    try:
        # chatdetails = await USER.get_chat(chid)
        await _.get_chat_member(chid, wew)
    except:
        for administrator in administrators:
            if administrator == message.from_user.id:
                if message.chat.title.startswith("Channel Music: "):
                    await lel.edit(
                        f"<b>tambahkan {user.first_name} ke saluran Anda.</b>",
                    )
                try:
                    invitelink = await _.export_chat_invite_link(chid)
                except:
                    await lel.edit(
                        "<b>jadikan saya sebagai admin terlebih dahulu.</b>",
                    )
                    return

                try:
                    await USER.join_chat(invitelink)
                    await USER.send_message(
                        message.chat.id,
                        "Saya bergabung ke grup ini untuk memutar musik di obrolan suara",
                    )
                    await lel.edit(
                        "<b>userbot bergabung dengan obrolan Anda</b>",
                    )

                except UserAlreadyParticipant:
                    pass
                except Exception:
                    # print(e)
                    await lel.edit(
                        f"<b>🔴 Flood Wait Error 🔴 \n{user.first_name} tidak dapat bergabung dengan group Anda karena banyaknya permintaan bergabung untuk assistant! Pastikan assistan tidak dibanned didalam grup."
                        f"\n\nAtau tambahkan @{user.username} Bot secara manual ke Group Anda dan coba lagi.</b>",
                    )
    try:
        await USER.get_chat(chid)
    # lmoa = await client.get_chat_member(chid,wew)
    except:
        await lel.edit(
            f"<b>{user.first_name}\nterkena banned dari Group ini, Minta admin untuk kirim perintah `/unban @{user.username}` di grup ini kemudian kirim perintah `/userbotjoin` di grup ini untuk mengundang assistant ke dalam grup anda</b>"
        )
        return
    text_links = None
    # await lel.edit("**🔎 Menemukan lagu...**")
    if message.reply_to_message:
        entities = []
        toxt = message.reply_to_message.text or message.reply_to_message.caption
        if message.reply_to_message.entities:
            entities = message.reply_to_message.entities + entities
        elif message.reply_to_message.caption_entities:
            entities = message.reply_to_message.entities + entities
        urls = [entity for entity in entities if entity.type == "url"]
        text_links = [entity for entity in entities if entity.type == "text_link"]
    else:
        urls = None
    if text_links:
        urls = True
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    rpk = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"

    audio = (
        (message.reply_to_message.audio or message.reply_to_message.voice)
        if message.reply_to_message
        else None
    )
    url = get_url(message)

    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"**❌ Lagu dengan durasi lebih dari `{DURATION_LIMIT}` menit tidak dapat diputar!\n🎧 Lagu yang di minta berdurasi `{duration}`**"
            )
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "💬 sᴜᴘᴘᴏʀᴛ", url=f"https://t.me/{SUPPORT_GROUP}"
                    ),
                    InlineKeyboardButton("ᴍᴇɴᴜ ⏯", callback_data="menu"),
                ],
            ]
        )
        file_name = get_file_name(audio)
        title = audio.title
        thumb_name = "https://telegra.ph/file/f6086f8909fbfeb0844f2.png"
        thumbnail = thumb_name
        duration = convert_seconds(audio.duration)
        views = "Locally added"
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await converter.convert(
            (await message.reply_to_message.download(file_name))
            if not path.isfile(path.join("downloads", file_name))
            else file_name
        )
    elif urls:
        query = toxt
        # await lel.edit("**🎵 Memproses lagu...**")
        ydl_opts = {
            "format": "bestaudio",
        }
        try:
            results = YoutubeSearch(query, max_results=1).to_dict()
            url = f"https://youtube.com{results[0]['url_suffix']}"
            title = results[0]["title"][:999]
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f"thumb{title}.jpg"
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, "wb").write(thumb.content)
            duration = results[0]["duration"]
            results[0]["url_suffix"]
            views = results[0]["views"]

        except Exception as e:
            await lel.edit(
                "**❌ Lagu tidak ditemukan**\nCoba masukan judul lagu yang lebih jelas"
            )
            print(str(e))
            return
        dlurl = url
        dlurl = dlurl.replace("youtube", "youtubepp")
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "💬 sᴜᴘᴘᴏʀᴛ", url=f"https://t.me/{SUPPORT_GROUP}"
                    ),
                    InlineKeyboardButton("ᴍᴇɴᴜ ⏯", callback_data="menu"),
                ],
            ]
        )
        requested_by = message.chat.title
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await converter.convert(youtube.download(url))
    else:
        query = ""
        for i in message.command[1:]:
            query += " " + str(i)
        print(query)
        # await lel.edit("**🎵 Memproses lagu...**")
        ydl_opts = {
            "format": "bestaudio",
        }

        try:
            results = YoutubeSearch(query, max_results=5).to_dict()
        except:
            await lel.edit("**anda tidak memberikan judul lagu apapun !**")
        # 𝗚𝗢𝗛𝗔𝗡 𝗠𝗨𝗦𝗜𝗖 tolol
        try:
            toxxt = f"**⚡ Silahkan pilih lagu yang ingin anda putar:** {rpk}\n\n"
            j = 0

            emojilist = [
                "1️⃣",
                "2️⃣",
                "3️⃣",
                "4️⃣",
                "5️⃣",
            ]
            while j < 5:
                toxxt += f"{emojilist[j]} [{results[j]['title'][:999]}](https://youtube.com{results[j]['url_suffix']})\n"
                toxxt += f"├ 💡 **Durasi:** {results[j]['duration']}\n"
                toxxt += f"└ ⚡ **Didukung:** [{bn}](t.me/{bu})\n\n"
                j += 1
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "1️⃣", callback_data=f"plll 0|{query}|{user_id}"
                        ),
                        InlineKeyboardButton(
                            "2️⃣", callback_data=f"plll 1|{query}|{user_id}"
                        ),
                        InlineKeyboardButton(
                            "3️⃣", callback_data=f"plll 2|{query}|{user_id}"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "4️⃣", callback_data=f"plll 3|{query}|{user_id}"
                        ),
                        InlineKeyboardButton(
                            "5️⃣", callback_data=f"plll 4|{query}|{user_id}"
                        ),
                    ],
                    [InlineKeyboardButton("❌", callback_data="close")],
                ]
            )
            await message.reply(
                toxxt,
                reply_markup=keyboard,
                disable_web_page_preview=True,
            )

            await lel.delete()
            # 𝗚𝗢𝗛𝗔𝗡 𝗠𝗨𝗦𝗜𝗖 tolol
            return
            # 𝗚𝗢𝗛𝗔𝗡 𝗠𝗨𝗦𝗜𝗖 tolol
        except:
            await lel.edit(f"**Tidak menemukan hasil apapun\nLangsung memutar lagu**")
            try:
                url = f"https://youtube.com{results[0]['url_suffix']}"
                title = results[0]["title"][:999]
                thumbnail = results[0]["thumbnails"][0]
                thumb_name = f"thumb{title}.jpg"
                thumb = requests.get(thumbnail, allow_redirects=True)
                open(thumb_name, "wb").write(thumb.content)
                duration = results[0]["duration"]
                results[0]["url_suffix"]
                views = results[0]["views"]
            except Exception as e:
                # await massage.delete()
                await lel.edit(
                    "**❌ lagu tidak ditemukan.** berikan nama lagu yang valid."
                )
                print(str(e))
                return
            dlurl = url
            dlurl = dlurl.replace("youtube", "youtubepp")

            requested_by = message.chat.title
            await generate_cover(requested_by, title, views, duration, thumbnail)
            file_path = await converter.convert(youtube.download(url))
    chat_id = get_chat_id(message.chat)
    if chat_id in callsmusic.pytgcalls.active_calls:
        position = await queues.put(chat_id, file=file_path)
        qeue = que.get(chat_id)
        s_name = title
        r_by = message.from_user
        loc = file_path
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)
        await message.reply_photo(
            photo="final.png",
            caption=f"""
**💡 Trek ditambahkan ke antrian

🏷 Nama: [{title}]({url})
⏱️ Durasi: {duration}
🎧 Atas permintaan: {message.from_user.mention}**
""",
            reply_markup=keyboard,
        )
        return await lel.delete()

    else:
        chat_id = get_chat_id(message.chat)
        que[chat_id] = []
        qeue = que.get(chat_id)
        s_name = title
        r_by = message.from_user
        loc = file_path
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)
        try:
            callsmusic.pytgcalls.join_group_call(chat_id, file_path)
        except:
            message.reply("**voice chat group tidak aktif, tidak dapat memutar lagu.**")
            return
        await message.reply_photo(
            photo="final.png",
            caption=f"""
**🏷 Nama: [{title}]({url})
⏱️ Durasi: {duration}
💡 Status: sedang memutar
🎧 Atas permintaan: {message.from_user.mention}**
""",
            reply_markup=keyboard,
        )
        return await lel.delete()


@Client.on_callback_query(filters.regex(pattern=r"plll"))
async def lol_cb(b, cb):
    global que
    cbd = cb.data.strip()
    chat_id = cb.message.chat.id
    typed_ = cbd.split(None, 1)[1]
    try:
        x, query, useer_id = typed_.split("|")
    except:
        await cb.message.edit("**❌ lagu tidak ditemukan**")
        return
    useer_id = int(useer_id)
    if cb.from_user.id != useer_id:
        await cb.answer(
            "anda bukan orang yang meminta untuk memutar lagu ini!", show_alert=True
        )
        return
    await cb.message.delete()
    # await cb.message.edit("**🔄 Sedang memproses lagu**")
    x = int(x)
    try:
        cb.message.reply_to_message.from_user.first_name
    except:
        cb.message.from_user.first_name
    results = YoutubeSearch(query, max_results=5).to_dict()
    resultss = results[x]["url_suffix"]
    title = results[x]["title"][:250]
    thumbnail = results[x]["thumbnails"][0]
    duration = results[x]["duration"]
    views = results[x]["views"]
    url = f"https://www.youtube.com{resultss}"
    try:
        secmul, dur, dur_arr = 1, 0, duration.split(":")
        for i in range(len(dur_arr) - 1, -1, -1):
            dur += int(dur_arr[i]) * secmul
            secmul *= 60
        if (dur / 60) > DURATION_LIMIT:
            await cb.message.edit(
                f"**❌ Lagu dengan durasi lebih dari `{DURATION_LIMIT}` menit tidak dapat diputar!\n🎧 Lagu yang di minta berdurasi `{duration}`**"
            )
            return
    except:
        pass
    try:
        thumb_name = f"thumb{title}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
    except Exception as e:
        print(e)
        return
    dlurl = url
    dlurl = dlurl.replace("youtube", "youtubepp")
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("💬 sᴜᴘᴘᴏʀᴛ", url=f"https://t.me/{SUPPORT_GROUP}"),
                InlineKeyboardButton("ᴍᴇɴᴜ ⏯", callback_data="menu"),
            ],
        ]
    )
    requested_by = cb.message.chat.title
    await generate_cover(requested_by, title, views, duration, thumbnail)
    file_path = await converter.convert(youtube.download(url))
    if chat_id in callsmusic.pytgcalls.active_calls:
        position = await queues.put(chat_id, file=file_path)
        qeue = que.get(chat_id)
        s_name = title
        try:
            r_by = cb.message.reply_to_message.from_user
        except:
            r_by = cb.message.from_user
        loc = file_path
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)
        await cb.message.reply_to_message.delete()
        await b.send_photo(
            chat_id,
            photo="final.png",
            caption=f"""
**💡 Trek ditambahkan ke antrian

🏷 Nama: [{title}]({url})
⏱️ Durasi: {duration}
🎧 Atas permintaan: {r_by.mention}**
""",
            reply_markup=keyboard,
        )
        os.remove("final.png")
    else:
        que[chat_id] = []
        qeue = que.get(chat_id)
        s_name = title
        try:
            r_by = cb.message.reply_to_message.from_user
        except:
            r_by = cb.message.from_user
        loc = file_path
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)
        callsmusic.pytgcalls.join_group_call(chat_id, file_path)
        await cb.message.delete()
        await cb.message.reply_to_message.delete()
        await b.send_photo(
            chat_id,
            photo="final.png",
            caption=f"""
**🏷 Nama: [{title}]({url})
⏱️ Durasi: {duration}
💡 Status: sedang memutar
🎧 Atas permintaan: {r_by.mention}**
""",
            reply_markup=keyboard,
        )
        os.remove("final.png")


@Client.on_message(
    command(["stream", f"stream@{bu}", "ytp", f"ytp@{bu}"]) & other_filters
)
@errors
async def ytp(_, message: Message):
    lel = await message.reply("**🔄 Memproses**")
    message.from_user.id
    message.from_user.first_name

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("💬 sᴜᴘᴘᴏʀᴛ", url=f"https://t.me/{SUPPORT_GROUP}"),
                InlineKeyboardButton("ᴛᴜᴛᴜᴘ 🗑", callback_data="close"),
            ],
        ]
    )

    audio = (
        (message.reply_to_message.audio or message.reply_to_message.voice)
        if message.reply_to_message
        else None
    )
    url = get_url(message)

    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"❌ Videos longer than {DURATION_LIMIT} minute(s) aren't allowed to play!"
            )

        file_name = get_file_name(audio)
        title = audio.title
        thumb_name = "https://telegra.ph/file/f6086f8909fbfeb0844f2.png"
        thumbnail = thumb_name
        duration = convert_seconds(audio.duration)
        views = message.from_user.first_name
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "💬 sᴜᴘᴘᴏʀᴛ", url=f"https://t.me/{SUPPORT_GROUP}"
                    ),
                    InlineKeyboardButton("ᴛᴜᴛᴜᴘ 🗑", callback_data="close"),
                ],
            ]
        )
        requested_by = message.chat.title
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await converter.convert(
            (await message.reply_to_message.download(file_name))
            if not path.isfile(path.join("downloads", file_name))
            else file_name
        )
    elif url:
        try:
            results = YoutubeSearch(query, max_results=1).to_dict()
            # url = f"https://youtube.com{results[0]['url_suffix']}"
            print(results)
            title = results[0]["title"][:999]
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f"thumb{title}.jpg"
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, "wb").write(thumb.content)
            duration = results[0]["duration"]
            results[0]["url_suffix"]
            views = results[0]["views"]
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "💬 sᴜᴘᴘᴏʀᴛ", url=f"https://t.me/{SUPPORT_GROUP}"
                        ),
                        InlineKeyboardButton("ᴛᴜᴛᴜᴘ 🗑", callback_data="close"),
                    ],
                ]
            )
        except Exception:
            title = "NaN"
            thumb_name = "https://telegra.ph/file/33fc5c8490eb948d1e816.jpg"
            duration = "NaN"
            views = "NaN"
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "💬 sᴜᴘᴘᴏʀᴛ", url=f"https://t.me/{SUPPORT_GROUP}"
                        ),
                        InlineKeyboardButton("ᴛᴜᴛᴜᴘ 🗑", callback_data="close"),
                    ],
                ]
            )
        requested_by = message.chat.title
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await converter.convert(youtube.download(url))
    else:
        await lel.edit("**🔎 Pencarian lagu **")
        message.from_user.id
        user_id = message.from_user.id
        message.from_user.first_name
        user_name = message.from_user.first_name
        rpk = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"

        query = ""
        for i in message.command[1:]:
            query += " " + str(i)
        print(query)
        await message.delete()
        await lel.edit("**🎵 Memproses lagu**")
        ydl_opts = {
            "format": "bestaudio",
        }
        try:
            results = YoutubeSearch(query, max_results=1).to_dict()
            url = f"https://youtube.com{results[0]['url_suffix']}"
            print(results)
            title = results[0]["title"][:999]
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f"thumb{title}.jpg"
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, "wb").write(thumb.content)
            duration = results[0]["duration"]
            results[0]["url_suffix"]
            views = results[0]["views"]

        except Exception as e:
            lel.edit(
                "❌ Lagu tidak ditemukan.\n\nCoba lagu lain atau mungkin mengejanya dengan benar."
            )
            print(str(e))
            return

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "💬 sᴜᴘᴘᴏʀᴛ", url=f"https://t.me/{SUPPORT_GROUP}"
                    ),
                    InlineKeyboardButton("ᴛᴜᴛᴜᴘ 🗑", callback_data="close"),
                ],
            ]
        )
        requested_by = message.chat.title
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await converter.convert(youtube.download(url))

    if message.chat.id in callsmusic.pytgcalls.active_calls:
        position = await queues.put(message.chat.id, file=file_path)
        await message.reply_photo(
            photo="final.png",
            caption=f"""
**💡 Trek ditambahkan ke antrian

🏷 Nama: [{title}]({url})
⏱️ Durasi: {duration}
🎧 Atas permintaan: {message.from_user.mention}**
""",
            reply_markup=keyboard,
        )
        os.remove("final.png")
        return await lel.delete()
    else:
        callsmusic.pytgcalls.join_group_call(message.chat.id, file_path)
        await message.reply_photo(
            photo="final.png",
            reply_markup=keyboard,
            caption=f"""
**🏷 Nama: [{title}]({url})
⏱️ Durasi: {duration}
💡 Status: sedang memutar
🎧 Atas permintaan: {message.from_user.mention}**
""",
        )
        os.remove("final.png")
        return await lel.delete()
