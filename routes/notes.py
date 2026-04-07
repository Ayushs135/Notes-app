from fastapi import APIRouter
from models.note import Note
from config.db import conn
from schemas.note import noteEntity, notesEntity
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


note = APIRouter()
templates = Jinja2Templates(directory="templates")

@note.get("/", response_class=HTMLResponse)
async def home(request: Request):
    docs = conn.notes.notes.find({})
    new_docs = []
    for doc in docs:
        new_docs.append({"id": doc["_id"], "title": doc["title"], "desc": doc["desc"], "important": doc["important"]})
    return templates.TemplateResponse(request=request, name="index.html", context={"request": request, "new_docs": new_docs})


@note.post("/")
async def addnote(request: Request):
    form = await request.form()
    form_dict = dict(form)
    important = form.get("important")
    if important == "on":
        important = True
    else:
        important = False
    conn.notes.notes.insert_one(form_dict)
    return {"Success": "Note added successfully"}