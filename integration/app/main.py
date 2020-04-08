from io import BytesIO

import requests
from starlette.responses import StreamingResponse
from fastapi import FastAPI, Request, Form, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.logger import logger

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/")
async def get_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/process_text")
async def process_text(text: str = Form(...)):
    req = requests.get("http://text2speech/text2speech", params={"text": text})
    fd = BytesIO(req.content)

    return StreamingResponse(fd, headers=req.headers, media_type=req.headers['Content-Type'])


@app.post("/process_audio")
async def process_audio(audio: UploadFile = File(...)):

    file_data = {'file': (audio.filename, audio.file, audio.content_type)}
    req = requests.post("http://speech2text/", files=file_data)

    response =  {"text": req.text}
    logger.info(response)
    return response


@app.post("/translate")
async def translate(text: str, source_language: str, target_language: str):

    return {"error": "Not yet implemented!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)