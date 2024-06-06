import os
import json
import random
import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI, File, Request, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from models.classify import classify_and_print_results

@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(process_audio_forever())
    yield
    # 這裡可以進行一些清理操作，如果需要的話

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

state = random.choice([1, 2])  # 初始狀態
result_json = None

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/state")
async def get_state():
    global result_json
    return {"state": state, "result": result_json}

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    with open(os.path.join('templates', 'output.wav'), "wb") as f:
        f.write(contents)
    return {"filename": file.filename}

async def process_audio_forever():
    global result_json, state
    model_path = os.path.join('templates', 'models', 'soundclassifier_with_metadata.tflite')
    labels_path = os.path.join('templates', 'models', 'labels.txt')
    audio_path = os.path.join('templates', 'output.wav')

    while True:
        if os.path.exists(audio_path):
            result_json = classify_and_print_results(model_path, labels_path, audio_path)
            result = json.loads(result_json)
            # 根據 result_json 中的 label_id 來設置 state
            if result['label_id'] == 1:
                state = 1
            elif result['label_id'] == 3:
                state = 2
        await asyncio.sleep(2)  # 每秒檢查一次
