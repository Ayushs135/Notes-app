from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
conn = MongoClient(os.getenv("MONGO_URL"))
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    docs = conn.notes.notes.find({})
    new_docs = []
    for doc in docs:
        new_docs.append({"id": doc["_id"], "note": doc["note"]})
    return templates.TemplateResponse(request=request, name="index.html", context={"request": request, "new_docs": new_docs})

@app.get("/items/{item_id}")
async def read_item_by_id(item_id: int):
    return {"item_id": item_id}