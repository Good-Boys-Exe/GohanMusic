from config import ASSISTANT_NAME as an
from config import BOT_NAME as bn


class Messages:
    HELPS_MSG = [
        ".",
        f"""
<b>👋🏻 Hallo Selamat Datang Kembali Di {bn}

✣️ {bn} Dapat Memutar Lagu Di Voice Chat Group Dengan Cara Yang Mudah.

✣️ Assistant Music » @{an}</b>
""",
        f"""
<b>Pengaturan
1) Jadikan Bot Sebagai Admin
2) Mulai Obrolan Suara / Vcg
3) Kirim Perintah /userbotjoin
• Jika Assistant Bot Bergabung Selamat Menikmati Musik, 
• Jika Assistant Bot Tidak Bergabung Silahkan Tambahkan @{an} Ke Grup Anda Dan Coba Lagi</b>
""",
        f"""
<b>Perintah semua anggota grup
• /play (judul lagu) - Untuk Memutar lagu yang Anda minta melalui YouTube
• /song (judul lagu) - Untuk Mendownload lagu dari YouTube
• /vsong (judul video) - Untuk Mendownload Video di YouTube
• /lyrics (judul lagu) Untuk Mencari Lirik Lagu
• /search (judul lagu/video) - Untuk Mencari Link Di YouTube Dengan Detail<b>
</b>\n\nPerintah semua admin grup
• /pause - Untuk Menjeda pemutaran Lagu
• /resume - Untuk Melanjutkan pemutaran Lagu yang di pause
• /skip - Untuk Menskip pemutaran lagu ke Lagu berikutnya
• /end - Untuk Memberhentikan pemutaran Lagu
• /reload - Untuk Segarkan daftar admin</b>
""",
    ]
