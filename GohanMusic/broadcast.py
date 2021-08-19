import asyncio

from pyrogram import Client, filters
from pyrogram.types import Message

from callsmusic.callsmusic import client as USER
from config import SUDO_USERS
from helpers.filters import command


@Client.on_message(command("pg") & filters.user(SUDO_USERS) & ~filters.edited)
async def broadcast(_, message: Message):
    sent = 0
    failed = 0
    if message.from_user.id not in SUDO_USERS:
        return
    wtf = await message.reply("`Mulai dari broadcast...`")
    if not message.reply_to_message:
        await wtf.edit("Mohon Balas Pesan ke ke pesan!")
        return
    lmao = message.reply_to_message.text
    async for dialog in USER.iter_dialogs():
        try:
            await USER.send_message(dialog.chat.id, lmao)
            sent = sent + 1
            await wtf.edit(
                f"`Broadcasting...` \n\n**Dikirim ke:** `{sent}` Obrolan \n**Gagal dikirim:** {failed} Obrolan"
            )
            await asyncio.sleep(3)
        except:
            failed = failed + 1
            await wtf.edit(
                f"`Broadcasting...` \n\n**Dikirim ke:** `{sent}` Obrolan \n**Gagal dikirim:** {failed} Obrolan"
            )

    return await wtf.edit(
        f"`Broadcast Selesai` \n\n**Dikirim ke:** `{sent}` Obrolan \n**Gagal dikirim:** {failed} Obrolan"
    )
