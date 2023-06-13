from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import HTMLResponse
import database

app = FastAPI()
DB_SESSION = None

@app.on_event("startup")
def on_startup():
    print('Hello World')
    global DB_SESSION
    DB_SESSION = database.get_db()


@app.get('/')
def home():
     return {'name': 'Videoapp'}


print(on_startup()) 