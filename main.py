from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
import yt_dlp
import requests

app = FastAPI()

@app.get("/stream")
def stream(id: str):

    yt_url = f"https://www.youtube.com/watch?v={id}"

    opts = {
        "quiet": True,
        "format": "best",
        "cookiefile": "cookies.txt",
        "extractor_args": {
            "youtube": {
                "player_client": ["android"]
            }
        }
    }

    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(yt_url, download=False)

    formats = info.get("formats", [])

    stream_url = None

    for f in reversed(formats):
        if f.get("url"):
            stream_url = f["url"]
            break

    if not stream_url:
        raise HTTPException(500, "No stream URL found")

    r = requests.get(
        stream_url,
        stream=True,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )

    return StreamingResponse(
        r.iter_content(chunk_size=65536),
        media_type="video/mp4",
        headers={
            "Access-Control-Allow-Origin": "*"
        }
    )
