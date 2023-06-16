import pathlib
import json
from fastapi import FastAPI
from fastapi import  Depends, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic.error_wrappers import ValidationError
from sqlalchemy.orm import Session
from videoapp import utils
from videoapp.users import models, schemas
from videoapp.shortcuts import render
from videoapp.database import engine, get_db

models.Base.metadata.create_all(bind=engine)  

BASE_DIR = pathlib.Path(__file__).resolve().parent
TEMPLATE_DIR  = BASE_DIR / "templates"

app = FastAPI()
templates = Jinja2Templates(directory=str(TEMPLATE_DIR))


@app.on_event("startup")
def on_startup():
    print('Hello World, Welcome to Video App')
    

@app.get('/', response_class=HTMLResponse)
def home(request: Request):
    context = {
        "abc": 123       
    }
    return render(request, "home.html", context)

@app.get('/login', response_class=HTMLResponse)
def login_get_view(request: Request):
   
    return render(request, "auth/login.html", {})


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
    return render(request, "auth/login.html", {"logged_in": True}, cookies=data)


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
    return render(request, "auth/signup.html", context)

@app.get("/users")
def users_list_view(db: Session = Depends(get_db)):
        q = db.query(models.User).limit(10)

        return list(q)












