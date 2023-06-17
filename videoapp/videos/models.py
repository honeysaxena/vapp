import uuid
from fastapi import Depends
from sqlalchemy import Column, String, UUID
from videoapp.database import Base, SessionLocal
from videoapp.users.models import User

from videoapp.videos.extractors import extract_video_id

class Video(Base):
    __tablename__ = "videos"
    host_id = Column(String, primary_key=True)
    db_id =  Column(UUID, primary_key=True, default=uuid.uuid1)
    host_service = Column(String, default='youtube')
    url = Column(String)
    user_id = Column(UUID)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"Video(email={self.email}, user_id={self.user_id})"
    

    @staticmethod
    def add_video(url, user_id=None):
        session = SessionLocal()
        host_id = extract_video_id(url)
        if host_id is None:
            raise Exception("Invalid Youtube Video URL")
        user_id = User.check_exists(user_id)
        if user_id is None:
            raise Exception("Invalid user_id")
        q = session.query(Video).filter_by(host_id=host_id, user_id=user_id)
        if q.count() != 0:
            raise Exception("Video already added!")
        session.close()
        return Video(host_id=host_id, user_id=user_id, url=url)
       

    



