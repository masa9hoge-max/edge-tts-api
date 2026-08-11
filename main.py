from fastapi import FastAPI, Response, HTTPException, Header
from pydantic import BaseModel
import edge_tts
import os
import secrets

app = FastAPI()

API_KEY = os.environ["API_KEY"]


class TTSRequest(BaseModel):
    text: str
    voice: str = "ja-JP-NanamiNeural"


@app.get("/")
def index():
    return {"status": "ok"}


@app.post("/tts")
async def tts(
    request: TTSRequest,
    x_api_key: str = Header(None)
):
    if not x_api_key or not secrets.compare_digest(x_api_key, API_KEY):
        raise HTTPException(status_code=401, detail="Invalid API key")

    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text is required")

    try:
        communicate = edge_tts.Communicate(
            request.text,
            request.voice
        )

        audio_data = bytearray()

        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data.extend(chunk["data"])

        return Response(
            content=bytes(audio_data),
            media_type="audio/mpeg"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
