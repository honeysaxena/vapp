import uuid
from typing import Optional
from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse
from videoapp.shortcuts import render, redirect, get_object_or_404, is_htmx
from videoapp.users.decorators import login_required
from videoapp import utils
from videoapp.videos.schemas import VideoCreateSchema
from videoapp.videos.models import Video
from videoapp.database import SessionLocal
from videoapp.watch_events.models import WatchEvent

router = APIRouter(
    prefix='/videos'
)


@router.get("/create", response_class=HTMLResponse)
@login_required
def video_create_view(request: Request, is_htmx=Depends(is_htmx), playlist_id: Optional[uuid.UUID] = None):
    print(playlist_id)
    if is_htmx:
        return render(request, "videos/htmx/create.html", {})
    return render(request, "videos/create.html", {})

@router.post("/create", response_class=HTMLResponse)
@login_required
def video_create_post_view(request: Request, is_htmx=Depends(is_htmx), title: str = Form(...), url: str = Form(...)):
    raw_data = {
        "title": title,
        "url": url,
        "user_id": request.user.username
    }

    data, errors = utils.valid_schema_data_or_error(raw_data, VideoCreateSchema)
    redirect_path = data.get('path') or "/videos/create"
    context = {
        "data": data,
        "errors": errors,
        "title": title,
        "url": url,
    }
    if is_htmx:
        """Handle all htmx requests"""
        if len(errors) > 0:
            return render(request, "videos/htmx/create.html", context)
        context = {
            "path": redirect_path,
            "title": data.get('title')
        }
        return render(request, "videos/htmx/link.html", context)
    """Handle default HTML requests"""
    
    if len(errors) > 0:
        return render(request, "videos/create.html", context, status_code=400)
    redirect_path = data.get('path') or "/videos/create"
    return redirect(redirect_path)

@router.get("/", response_class=HTMLResponse)
def video_list_view(request: Request):
    session = SessionLocal()
    q = session.query(Video).limit(100)
    context = {
        "object_list": q
    }
    session.close()
    return render(request, "videos/list.html", context)


@router.get("/{host_id}", response_class=HTMLResponse)
def video_detail_view(request: Request, host_id: str):
    q = get_object_or_404(Video, host_id=host_id)
    start_time = 0
    if request.user.is_authenticated:
        user_id = request.user.username
        start_time = WatchEvent.get_resume_time(host_id, user_id)
    
    for obj in q:

        context = {
            "host_id": host_id,
            "start_time": start_time,
            "object": obj or None   
        }
    print(context)
    return render(request, "videos/detail.html", context)



