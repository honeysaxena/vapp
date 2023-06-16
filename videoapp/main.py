import pathlib
from fastapi import FastAPI
from fastapi import  Depends, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from videoapp.users import models
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
        "request": request,
        "abc": 123       
     }
     return templates.TemplateResponse("home.html", context)

@app.get('/login', response_class=HTMLResponse)
def login_get_view(request: Request):
   
    return templates.TemplateResponse("auth/login.html", {
        "request": request,
    })

@app.post('/login', response_class=HTMLResponse)
def login_post_view(request: Request, email: str = Form(...), password: str = Form(...)):
    print(email, password)
    return templates.TemplateResponse("auth/signup.html", {
        "request": request,
    })

@app.get('/signup', response_class=HTMLResponse)
def signup_get_view(request: Request):
   
    return templates.TemplateResponse("auth/signup.html", {
        "request": request,
    })

@app.post('/signup', response_class=HTMLResponse)
def signup_post_view(request: Request, email: str = Form(...), password: str = Form(...), password_confirm: str = Form(...)):
    
    return templates.TemplateResponse("auth/login.html", {
        "request": request,
    })

@app.get("/users")
def users_list_view(db: Session = Depends(get_db)):
        q = db.query(models.User).limit(10)

        return list(q)












