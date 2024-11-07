from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import yt_dlp

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class VideoResponse(BaseModel):
    title: str
    url: str
    duration: int
    formats: list

@app.get("/video-info/")
async def get_video_info(url: str):
    """Get video information and available formats"""
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # Filter for audio-only formats
            audio_formats = [
                format for format in info['formats'] 
                if format.get('acodec') != 'none' and format.get('vcodec') == 'none'
            ]
            
            return {
                "title": info['title'],
                "duration": info['duration'],
                "formats": audio_formats
            }
            
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))