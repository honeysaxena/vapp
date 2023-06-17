from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from videoapp.shortcuts import render


router = APIRouter(
    prefix='/videos'
)


@router.get("/", response_class=HTMLResponse)
def video_list_vies(request: Request):
    return render(request, "videos/list.html", {})


@router.get("/detail", response_class=HTMLResponse)
def video_detail_vies(request: Request):
    return render(request, "videos/detail.html", {})

