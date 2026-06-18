from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import subprocess
import uuid
import os

app = FastAPI()

UPLOAD_DIR = "app/uploads"
OUTPUT_DIR = "app/outputs"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.post("/convert-mp3")
async def convert_mp3(file: UploadFile = File(...)):
    uid = str(uuid.uuid4())

    input_path = f"{UPLOAD_DIR}/{uid}_{file.filename}"
    output_path = f"{OUTPUT_DIR}/{uid}.mp3"

    with open(input_path, "wb") as f:
        f.write(await file.read())

    subprocess.run(
        ["ffmpeg", "-i", input_path, "-vn", "-y", output_path],
        check=True
    )

    return FileResponse(
        output_path,
        media_type="audio/mpeg",
        filename="audio.mp3"
    )
