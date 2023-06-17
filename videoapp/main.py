import pathlib
import json
from fastapi import FastAPI
from fastapi import  Depends, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic.error_wrappers import ValidationError
from sqlalchemy.orm import Session
from videoapp import utils
from videoapp.users import models, schemas
from videoapp.shortcuts import render, redirect
from videoapp.database import engine, get_db
from videoapp.users.decorators import login_required

models.Base.metadata.create_all(bind=engine)  

BASE_DIR = pathlib.Path(__file__).resolve().parent
TEMPLATE_DIR  = BASE_DIR / "templates"

app = FastAPI()
templates = Jinja2Templates(directory=str(TEMPLATE_DIR))

from videoapp.handlers import * # noqa


@app.on_event("startup")
def on_startup():
    print('Hello World, Welcome to Video App')
    

@app.get('/', response_class=HTMLResponse)
def home(request: Request):
    context = {
        "abc": 123       
    }
    return render(request, "home.html", context)

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












