from fastapi import FastAPI, Response, HTTPException
import edge_tts

app = FastAPI()

@app.get("/")
def index():
    return {"status": "ok", "message": "edge-tts API is running!"}

@app.get("/tts")
async def tts(text: str, voice: str = "ja-JP-NanamiNeural"):
    if not text:
        raise HTTPException(status_code=400, detail="Text parameter is required")
    
    try:
        communicate = edge_tts.Communicate(text, voice)
        audio_data = bytearray()
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data.extend(chunk["data"])
        return Response(content=bytes(audio_data), media_type="audio/mpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
