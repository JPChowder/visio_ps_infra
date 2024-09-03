from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
from google.cloud import storage
from pathlib import Path
import os
import subprocess

from utils import VideoDownloader
from reencoder import VP8Reencoder, VP9Reencoder, AV1Reencoder

app = FastAPI()
# Para rodar a API usamos 'uvicorn api:app'

class VideoRequest(BaseModel):
    video_source: str # camnho na GCP

def reencode_video(video_path: str, output_path: str, reencoder_class):
    # Parametros retirados das variaveis de ambiente
    crf = int(os.getenv("CRF", "30"))    # Default 30
    speed = int(os.getenv("SPEED", "2")) # Default 2
    bitrate = os.getenv("BITRATE", None) # Sem valor dafault (constant quality)

    reencoder = reencoder_class(video_path, output_path, crf=crf, speed=speed, bitrate=bitrate)
    reencoder.reencode()

@app.post("/reencode/")
async def reencode_video_endpoint(video_request: VideoRequest, background_tasks: BackgroundTasks):
    downloader = VideoDownloader()
    video_source = video_request.video_source
    download_path = "/tmp/downloaded_video.mp4"
    try:
        download_path = downloader.download_video(video_source, "/tmp")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error downloading video: {str(e)}")

    output_path = "/tmp/reencoded_video.mp4"
    
    # A funcao globals() procura na tabela global de simbolos por algo com o nome fornecido,
    # no caso uma classe e permite que a variavel reencoder_class a instancie dinamicamente
    reencoder_class_name = os.getenv("REENCODER_CLASS_NAME", "VP9Reencoder") # Default VP9
    reencoder_class = globals().get(reencoder_class_name)

    if not reencoder_class:
        raise HTTPException(status_code=400, detail=f"Reencoder class {reencoder_class_name} not found")

    # Faz o reencoding no background background
    background_tasks.add_task(reencode_video, video_path=download_path, output_path=output_path, reencoder_class=reencoder_class)
    
    return {"message": "Video reencoding started", "output_path": output_path}

