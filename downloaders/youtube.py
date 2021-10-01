from os import path

from youtube_dl import YoutubeDL

from config import DURATION_LIMIT
from helpers.errors import DurationLimitError

ydl_opts = {
    "format": "bestaudio/best",
    "verbose": True,
    "geo-bypass": True,
    "nocheckcertificate": True,
    "addmetadata": True,
    "key": "FFmpegMetadata",
    "prefer_ffmpeg": True,
    "nocheckcertificate": True,
    "outtmpl": "downloads/%(id)s.%(ext)s",
}

ydl = YoutubeDL(ydl_opts)


def download(url: str) -> str:
    info = ydl.extract_info(url, download=True)
    duration = round(info["duration"] / 60)

    if duration > DURATION_LIMIT:
        raise DurationLimitError(
            f"❌ Video lebih panjang dari {DURATION_LIMIT} menit tidak diperbolehkan, video yang disediakan adalah {duration} menit)"
        )
    try:
        ydl.download([url])
    except:
        raise DurationLimitError(
            f"❌ Video lebih panjang dari {DURATION_LIMIT} menit tidak diperbolehkan, video yang disediakan adalah {duration} menit)"
        )
    return path.join("downloads", f"{info['id']}.{info['ext']}")
