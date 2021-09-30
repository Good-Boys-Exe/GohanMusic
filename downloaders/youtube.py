from os import path

from youtube_dl import YoutubeDL

from config import DURATION_LIMIT
from helpers.errors import DurationLimitError

ydl_opts = {
        "format": "bestaudio",
        "addmetadata": True,
        "key": "FFmpegMetadata",
        "writethumbnail": True,
        "prefer_ffmpeg": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "720",
            }
        ],
        "outtmpl": "%(id)s.mp3",
        "quiet": True,
        "logtostderr": False,
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
