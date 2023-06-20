import uuid
from fastapi import Depends
from sqlalchemy import Column, String, UUID, Text
from videoapp.users.exceptions import InvalidUserIDException
from videoapp.database import Base, SessionLocal
from videoapp.users.models import User
from videoapp.videos.exceptions import InvalidYoutubeVideoURLException, VideoAlreadyAddedException
from videoapp.videos.extractors import extract_video_id
from videoapp.shortcuts import templates


class Video(Base):
    __tablename__ = "videos"
    host_id = Column(String, primary_key=True)
    db_id =  Column(UUID, primary_key=True, default=uuid.uuid1)
    host_service = Column(String, default='youtube')
    title = Column(Text)
    url = Column(String)
    user_id = Column(UUID)  

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"Video(title={self.title}, host_id={self.host_id}, host_service={self.host_service})"
    
    def render(self):
        basename = self.host_service
        template_name = f"videos/renderers/{basename}.html"
        context = {"host_id": self.host_id}
        t = templates.get_template(template_name)
        return t.render(context)

    def as_data(self):
        return {f"{self.host_service}_id": self.host_id, "path": self.path}
    
    @property
    def path(self):
        return f"/videos/{self.host_id}"

    @staticmethod
    def add_video(url, user_id=None, **kwargs):
        session = SessionLocal()
        host_id = extract_video_id(url)
        if host_id is None:
            raise InvalidYoutubeVideoURLException("Invalid Youtube Video URL")
        user_exists = User.check_exists(user_id)
        if user_exists is False:
            raise InvalidUserIDException("Invalid user_id")
        q = session.query(Video).filter_by(host_id=host_id)
        if q.count() != 0:
            raise VideoAlreadyAddedException("Video already added!")
        
        obj = Video(host_id=host_id, user_id=user_id, url=url, **kwargs)
        session.add(obj)
        session.commit()
        session.refresh(obj)
        session.close()
        return obj
    
    
       

    



