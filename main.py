from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import StreamingResponse
import yt_dlp
import requests

app = FastAPI()

def get_direct(video_url):
    opts = {
        "quiet": True,
        "format": "best",
        "cookiefile": "cookies.txt"
    }   
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(video_url, download=False)

        formats = info.get("formats", [])

        for f in reversed(formats):
            if f.get("url"):
                return f["url"]

    raise Exception("No stream URL")


@app.get("/stream")
def stream(id: str = Query(...)):

    yt = f"https://www.youtube.com/watch?v={id}"

    direct = get_direct(yt)

    r = requests.get(
        direct,
        stream=True,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )

    return StreamingResponse(
        r.iter_content(65536),
        media_type="video/mp4",
        headers={
            "Access-Control-Allow-Origin": "*"
        }
    )
