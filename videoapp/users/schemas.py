from pydantic import BaseModel, EmailStr, SecretStr, validator
from videoapp.users.models import User
from videoapp.database import SessionLocal

class UserSignupSchema(BaseModel):
    email: EmailStr
    password: SecretStr
    password_confirm: SecretStr
        
    @validator("email")
    def email_validator(cls, v, values, **kwargs):
        session = SessionLocal()
        #yield session
        q = session.query(User).filter_by(email=v)
        if q.count() != 0:
            raise ValueError('Email is not available')
        session.close()
        return v    
        
    @validator("password_confirm")
    def password_match(cls, v, values, **kwargs):
        password = values.get('password')
        password_confirm = v
        if password != password_confirm:
            raise ValueError("Password do not match")
        return v 