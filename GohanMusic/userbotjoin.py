import asyncio

from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant

from callsmusic.callsmusic import client as USER
from config import BOT_USERNAME, SUDO_USERS
from helpers.decorators import authorized_users_only, errors
from helpers.filters import command


@Client.on_message(
    command(["userbotjoin", f"userbotjoin@{BOT_USERNAME}"]) & filters.group
)
@authorized_users_only
@errors
async def addchannel(client, message):
    chid = message.chat.id
    try:
        invitelink = await client.export_chat_invite_link(chid)
    except:
        await message.reply_text(
            "<b>Tambahkan saya sebagai admin group Anda terlebih dahulu.</b>",
        )
        return
    try:
        user = await USER.get_me()
    except:
        user.first_name = "helper"
    try:
        await USER.join_chat(invitelink)
        await USER.send_message(
            message.chat.id, "Saya bergabung di sini seperti yang Anda minta"
        )
    except UserAlreadyParticipant:
        await message.reply_text(
            f"<b>{user.first_name} sudah ada di obrolan Anda.</b>",
        )
    except Exception as e:
        print(e)
        await message.reply_text(
            f"<b>🛑 Flood Wait Error 🛑 \n{user.first_name} tidak dapat bergabung dengan group Anda karena banyaknya permintaan bergabung untuk userbot! Pastikan pengguna tidak dibanned dalam group."
            f"\n\nAtau tambahkan @{user.username} secara manual ke Group Anda dan coba lagi.</b>",
        )
        return
    await message.reply_text(
        f"<b>{user.first_name} berhasil bergabung dengan group Anda.</b>",
    )


@USER.on_message(command("userbotleave") & filters.group)
async def rem(USER, message):
    try:
        await USER.leave_chat(message.chat.id)
    except:
        await message.reply_text(
            "<b>Pengguna tidak dapat meninggalkan group Anda! Mungkin menunggu floodwaits."
            "\n\nAtau keluarkan saya secara manual dari ke Group Anda</b>",
        )
        return


@Client.on_message(
    command("userbotleaveall") & filters.user(SUDO_USERS) & ~filters.edited
)
async def bye(client, message):
    if message.from_user.id in SUDO_USERS:
        left = 0
        failed = 0
        lol = await message.reply("Asisten Meninggalkan semua obrolan")
        async for dialog in USER.iter_dialogs():
            try:
                await USER.leave_chat(dialog.chat.id)
                left = left + 1
                await lol.edit(
                    f"Asisten pergi... Meninggalkan: {left} obrolan Gagal: {failed} obrolan."
                )
            except:
                failed = failed + 1
                await lol.edit(
                    f"Asisten pergi... Meninggalkan: {left} obrolan Gagal: {failed} obrolan."
                )
            await asyncio.sleep(0.7)
        await client.send_message(
            message.chat.id, f"Keluar {left} obrolan gagal {failed} obrolan."
        )
