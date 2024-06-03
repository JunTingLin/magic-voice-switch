from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()
templates = Jinja2Templates(directory="templates/")

# 靜態文件設置
app.mount("/static", StaticFiles(directory="templates"), name="static")

# 燈的初始狀態
light_status = False

# 定義首頁路由
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "status": "開" if light_status else "關"})

# 定義切換燈的路由
@app.post("/toggle_light")
async def toggle_light():
    global light_status
    light_status = not light_status
    return {"status": "開" if light_status else "關"}
