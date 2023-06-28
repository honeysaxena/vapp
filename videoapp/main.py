import pathlib
#import json
from typing import Optional
from fastapi import FastAPI
from fastapi import  Depends, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.authentication import requires
#from pydantic.error_wrappers import ValidationError
from sqlalchemy.orm import Session
from videoapp import utils
#from videoapp.playlists.routers import router as playlist_router
from videoapp.users import models, schemas
from videoapp.shortcuts import render, redirect
from videoapp.database import get_db, create_db_and_tables
from videoapp.users.decorators import login_required
from videoapp.users.backends import JWTCookieBackend
#from videoapp.videos.models import Video
from videoapp.videos.routers import router as video_router
#from videoapp.watch_events.models import WatchEvent
from videoapp.watch_events.routers import router as watch_event_router
#from videoapp.playlists.models import Playlists
from indexing.client import update_index, search_index

 

BASE_DIR = pathlib.Path(__file__).resolve().parent

app = FastAPI()
app.add_middleware(AuthenticationMiddleware, backend=JWTCookieBackend())
#app.include_router(playlist_router)
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
    return render(request, "auth/login.html", {})


@app.post('/login', response_class=HTMLResponse)
def login_post_view(request: Request, email: str = Form(...), password: str = Form(...), next: Optional[str] = "/"):
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
    if "http://127.0.0.1" not in next:
        next = '/'
    return redirect(next, cookies=data)

@app.get('/logout', response_class=HTMLResponse)
def logout_get_view(request: Request):
    if not request.user.is_authenticated:
        return redirect('/login')
    return render(request, "auth/logout.html", {})

@app.post('/logout', response_class=HTMLResponse)
def logout_post_view(request: Request):
    return redirect("/login", remove_session=True)

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


@app.post('/update-index', response_class=HTMLResponse)
def htmx_update_index_view(request: Request):
    count = update_index()
    return HTMLResponse(f"({count}) Refreshed")


@app.get("/search", response_class=HTMLResponse)
def search_detail_view(request: Request,  q:Optional[str] = None):
    query = None
    context = {}
    if q is not None:
        query = q
        results = search_index(query)
        hits = results.get('hits') or []
        num_hits = results.get('nbHits')
        context = {
            "query": query,
            "hits": hits,
            "num_hits": num_hits
        }
    return render(request, "search/detail.html", context)

















