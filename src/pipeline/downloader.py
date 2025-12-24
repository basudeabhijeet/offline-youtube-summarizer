import os
import yt_dlp

def download_audio(url, output_dir):
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(output_dir, "%(id)s.%(ext)s"),
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "wav",
        }],
        # Limit to videos under 10 minutes (safe & professional)
        "match_filter": yt_dlp.utils.match_filter_func("duration < 600"),
        "quiet": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        video_id = info["id"]

    return os.path.join(output_dir, f"{video_id}.wav")
