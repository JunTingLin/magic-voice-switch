import os
import random

from fastapi import FastAPI, File, Request, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from models.classify import classify_and_print_results

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# @api
@app.get("/api/state")
async def get_state():
    result_json = classify_and_print_results(
        model_path=os.path.join('templates', 'models', 'soundclassifier_with_metadata.tflite'), 
        labels_path=os.path.join('templates', 'models', 'labels.txt'),
        audio_path=os.path.join('templates', 'output.wav')
    )
    print(result_json)
    # TODO 把 result 給抽離出來
    return {"state": random.choice([1, 2])}

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    with open(os.path.join('templates', 'output.wav'), "wb") as f:
        f.write(contents)
    return {"filename": file.filename}
