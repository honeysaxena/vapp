import uuid
from fastapi import Depends
from sqlalchemy import Column, String, UUID
from videoapp.database import Base, SessionLocal
from videoapp.users import validators, security



class User(Base):
    __tablename__ = "users"
    email = Column(String, primary_key=True)
    user_id =  Column(UUID, primary_key=True, default=uuid.uuid1)
    password = Column(String)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"User(email={self.email=}, user_id={self.user_id})"
    

    def set_password(self, pw, commit=False):
        pw_hash = security.generate_hash(pw)
        self.password = pw_hash
        if commit:
            self.save()
        return True 

    def verify_password(self, pw_str):
        pw_hash = self.password
        verified, _ = security.verify_hash(pw_hash, pw_str)
        return verified   

    @staticmethod
    def create_user(email: String, password: String = None):
        session = SessionLocal()
        yield session
        q = session.query(User).filter(User.email==email)
        print(q)
        if q.count() != 0:
            raise Exception("user already has account with this email")
        valid, msg, email = validators._validate_email(email)
        if not valid:
            raise Exception(f'Invalid email: {msg}')
        obj = User(email=email)
        obj.set_password(password)
        #obj.password = password
        session.add(obj)
        session.commit()
        session.refresh(obj)
        session.close()
        return obj


    @staticmethod
    def check_exists(user_id):
        session = SessionLocal()
        q = session.query(User).filter_by(user_id=user_id)
        session.close()
        return q.count() != 0


    @staticmethod
    def by_user_id(user_id=None):
        session = SessionLocal()
        if user_id is None:
            return None
        q = session.query(User).filter_by(user_id=user_id)
        if q.count() != 1:
            return None
        return q.first()



#user1 = User.create_user(email='abc@gmail.com', password='abc123')
#print(user1)


