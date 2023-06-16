import datetime
from jose import jwt, ExpiredSignatureError
from videoapp.users.models import User
from fastapi import Depends
from sqlalchemy.orm import Session
from videoapp.database import get_db
from videoapp.config import settings


def authenticate(email, password, db: Session = Depends(get_db)):
    try:
        user_obj = db.query(User).filter_by(email=email)
    except Exception as e:
        user_obj = None    
    if not user_obj.verify_password(password):
        return None
    return user_obj

def login(user_obj, expires_after=86400):
    raw_data = {
    "user_id": f"{user_obj.user_id}",
    "role": "admin",    
    "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_after)
    }
    return jwt.encode(raw_data, settings.secret_key, algorithm=settings.jwt_algorithm)

def verify_user_id(token):
    data = {}
    try:
        data = jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])
    except ExpiredSignatureError as e:
        print(e, "log out user")
    except:
        pass
    if "user_id" not in data:
        return None       
    return data    