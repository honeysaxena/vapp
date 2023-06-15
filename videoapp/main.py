from fastapi import FastAPI
from fastapi import Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from videoapp.users import models
from videoapp.database import engine, get_db

models.Base.metadata.create_all(bind=engine)    


app = FastAPI()


@app.on_event("startup")
def on_startup():
    print('Hello World')
    

@app.get('/')
def home():
     return {'name': 'Videoapp'}

@app.get("/users")
def users_list_view(session: Session = Depends(get_db)):
        q = session.query(models.User).limit(10)

        return list(q)












