'''
from datetime import datetime
import uuid
from typing import List
from sqlalchemy import Column, DateTime, UUID, Text, String
from sqlalchemy.types import Text
#from sqlalchemy.orm import Mapped, relationship, mapped_column
from videoapp.database import Base, engine, session
from videoapp.videos.models import Video
from sqlalchemy.ext.mutable import MutableList

Base.metadata.create_all(bind=engine)  


class Playlists(Base):
    __tablename__ = "playlists"
    db_id = Column(UUID, primary_key=True, default=uuid.uuid1)
    user_id = Column(String)
    updated = Column(DateTime, default=datetime.utcnow())
    title = Column(Text)
    #host_ids = Column(MutableList.as_mutable(String), default=[])
    _host_ids = Column(String, default='')

   
    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"Playlists(db_id={self.db_id}, user_id={self.user_id}, updated={self.updated}, host_ids={self.host_ids}, title={self.title})"

    @property
    def host_ids(self):
        return [str(x) for x in self._host_ids.split(',')]

    @property
    def path(self):
        return f"/playlists/{self.db_id}"

    @host_ids.setter
    def add_host_ids(self, _host_ids='', replace_all=False):
        if not isinstance(_host_ids, str):
            return False
        if replace_all:
            self._host_ids = _host_ids
        else:
            self._host_ids += _host_ids
            
        self.updated = datetime.utcnow()
        session.commit()
        session.close()
        print(_host_ids)
        return _host_ids
    
    
    def get_videos(self):
        session = SessionLocal()
        videos = []
        for host_id in self.host_ids:
            
            try:
                #video_obj = session.get(Video, {"host_id": host_id})
                video_obj = session.query(Video).filter_by(host_id=host_id)
                for obj in video_obj:
                    videos.append(obj)
                    #pass
            except:
                obj = None
            #if obj is not None:
            #    videos.append(obj)
        session.close()           
        return videos
'''    


    
