import uuid
from sqlalchemy import Column, String, UUID
from videoapp.database import Base, engine


Base.metadata.create_all(bind=engine)


class User(Base):
    __tablename__ = "users"
    email = Column(String, primary_key=True)
    user_id =  Column(UUID, primary_key=True, default=uuid.uuid1)
    password = Column(String)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"User(email={self.email=}, user_id={self.user_id})"