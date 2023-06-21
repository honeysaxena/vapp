import uuid
from starlette.exceptions import HTTPException
from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse
from videoapp.shortcuts import render, redirect, get_object_or_404, is_htmx
from videoapp.users.decorators import login_required
from videoapp import utils
from videoapp.playlists.schemas import PlaylistsCreateSchema, PlaylistVideoAddSchema
from videoapp.videos.schemas import VideoCreateSchema
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
    session = SessionLocal()
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
    session.add(obj)
    session.commit()
    session.refresh(obj)
    session.close()
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

@router.get("/{db_id}/add-video", response_class=HTMLResponse)
@login_required
def playlist_video_add_view(request: Request, db_id: uuid.UUID, is_htmx=Depends(is_htmx)):
    context = {"db_id": db_id}
    if not is_htmx:
        raise HTTPException(status_code=400)
    return render(request, "playlists/htmx/add-video.html", context)

@router.post("/{db_id}/add-video", response_class=HTMLResponse)
@login_required
def playlist_video_add_post_view(request: Request, db_id: uuid.UUID, is_htmx=Depends(is_htmx), title: str = Form(...), url: str = Form(...)):
    raw_data = {
        "title": title,
        "url": url,
        "user_id": request.user.username,
        "playlist_id": db_id
    }

    data, errors = utils.valid_schema_data_or_error(raw_data, PlaylistVideoAddSchema)
    redirect_path = data.get('path') or f"/videos/{db_id}"
    context = {
        "data": data,
        "errors": errors,
        "title": title,
        "url": url,
        "db_id": db_id
    }
    if not is_htmx:
        raise HTTPException(status_code=400)
    """Handle all htmx requests"""
    if len(errors) > 0:
        return render(request, "playlists/htmx/add-video.html", context)
    context = {
        "path": redirect_path,
        "title": data.get('title')
    }
    return render(request, "videos/htmx/link.html", context)
    

