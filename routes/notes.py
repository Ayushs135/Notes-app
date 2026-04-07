from fastapi import APIRouter
from models.note import Note
from config.db import conn
from schemas.note import noteEntity, notesEntity
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

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

    note_data = {
        "title": form.get("title"),
        "desc": form.get("desc"),
        "important": True if form.get("important") == "on" else False
    }

    conn.notes.notes.insert_one(note_data)

    from fastapi.responses import RedirectResponse
    return RedirectResponse("/", status_code=303)