import uuid
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from videoapp.shortcuts import render, redirect, get_object_or_404
from videoapp.users.decorators import login_required
from videoapp import utils
from videoapp.playlists.schemas import PlaylistsCreateSchema
from videoapp.playlists.models import Playlists
from videoapp.database import SessionLocal

router = APIRouter(
    prefix='/playlists'
)

@router.get("/create", response_class=HTMLResponse)
@login_required
def playlist_create_view(request: Request):
    return render(request, "playlists/create.html", {})

@router.post("/create", response_class=HTMLResponse)
@login_required
def playlist_create_post_view(request: Request, title: str = Form(...)):
    raw_data = {
        "title": title,
        "user_id": request.user.username
    }

    data, errors = utils.valid_schema_data_or_error(raw_data, PlaylistsCreateSchema)
    context = {
        "data": data,
        "errors": errors,
    }
    if len(errors) > 0:
        return render(request, "playlists/create.html", context, status_code=400)
    obj = Playlists(**data)
    redirect_path = obj.path or "/playlists/create"
    return redirect(redirect_path)

@router.get("/", response_class=HTMLResponse)
def playlist_list_view(request: Request):
    session = SessionLocal()
    q = session.query(Playlists).limit(100)
    context = {
        "object_list": q
    }
    session.close()
    return render(request, "playlists/list.html", context)


@router.get("/{db_id}", response_class=HTMLResponse)
def playlist_detail_view(request: Request, db_id: uuid.UUID):
    q = get_object_or_404(Playlists, db_id=db_id)
    if request.user.is_authenticated:
        user_id = request.user.username
    
    for obj in q:

        context = {
            "object": obj or None,
            "videos": obj.get_videos(),   
        }
    print(context)
    return render(request, "playlists/detail.html", context)



