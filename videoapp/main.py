import pathlib
import json
from fastapi import FastAPI
from fastapi import  Depends, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.authentication import requires
from pydantic.error_wrappers import ValidationError
from sqlalchemy.orm import Session
from videoapp import utils
from videoapp.playlists.routers import router as playlist_router
from videoapp.users import models, schemas
from videoapp.shortcuts import render, redirect
from videoapp.database import get_db, SessionLocal, create_db_and_tables
from videoapp.users.decorators import login_required
from videoapp.users.backends import JWTCookieBackend
#from videoapp.videos.models import Video
from videoapp.videos.routers import router as video_router
#from videoapp.watch_events.models import WatchEvent
from videoapp.watch_events.routers import router as watch_event_router
from videoapp.playlists.models import Playlists

 

BASE_DIR = pathlib.Path(__file__).resolve().parent

app = FastAPI()
app.add_middleware(AuthenticationMiddleware, backend=JWTCookieBackend())
app.include_router(playlist_router)
app.include_router(video_router)
app.include_router(watch_event_router)

from videoapp.handlers import * # noqa


@app.on_event("startup")
def on_startup():
    print('Hello World, Welcome to Video App')
    create_db_and_tables()
    

@app.get('/', response_class=HTMLResponse)
def home(request: Request):
    if request.user.is_authenticated:
        return render(request, "dashboard.html", {}, status_code=200 )
    print(request.user)
    print(request.user.is_authenticated)
    return render(request, "home.html", {})

# account page
@app.get('/account', response_class=HTMLResponse)
@login_required
def account_view(request: Request):
    """
    hello world!
    """
    context = {}
    return render(request, "account.html", context)


@app.get('/login', response_class=HTMLResponse)
def login_get_view(request: Request):
    session_id  = request.cookies.get("session_id") or None
    return render(request, "auth/login.html", {"logged_in": session_id is not None})


@app.post('/login', response_class=HTMLResponse)
def login_post_view(request: Request, email: str = Form(...), password: str = Form(...)):
    raw_data = {
         "email": email,
         "password": password,
    }
    data, errors = utils.valid_schema_data_or_error(raw_data, schemas.UserLoginSchema)
    context = {
        "data": data,
        "errors": errors,
        }
    if len(errors) > 0:
        return render(request, "auth/login.html", context, status_code=400)       
    #print(data['password'].get_secret_value())
    return redirect("/", cookies=data)


@app.get('/signup', response_class=HTMLResponse)
def signup_get_view(request: Request):
   
    return render(request, "auth/signup.html", {})


@app.post('/signup', response_class=HTMLResponse)
def signup_post_view(request: Request, email: str = Form(...), password: str = Form(...), password_confirm: str = Form(...)):
    raw_data = {
         "email": email,
         "password": password,
         "password_confirm": password_confirm
    }
    data, errors = utils.valid_schema_data_or_error(raw_data, schemas.UserSignupSchema)       
    context = {
        "data": data,
        "errors": errors,
    }
    if len(errors) > 0:
        return render(request, "auth/signup.html", context, status_code=400)  
    return redirect("/login")

@app.get("/users")
def users_list_view(db: Session = Depends(get_db)):
        q = db.query(models.User).limit(10)

        return list(q)

















