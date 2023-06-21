from datetime import datetime
import uuid
from sqlalchemy import Column, DateTime, UUID, Text, PickleType, Integer, UUID
from sqlalchemy.ext.mutable import MutableList
from videoapp.database import Base, SessionLocal, engine
from videoapp.videos.models import Video

Base.metadata.create_all(bind=engine)  


class Playlists(Base):
    __tablename__ = "playlists"
    db_id = Column(UUID, primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID)
    updated = Column(DateTime, default=datetime.utcnow())
    host_ids = Column(MutableList.as_mutable(PickleType), default=[])
    title = Column(Text)

    @property
    def path(self):
        return f"/playlists/{self.db_id}"

    def add_host_ids(self, host_ids=[], replace_all=False):
        session = SessionLocal()
        if not isinstance(host_ids, list):
            return False
        if replace_all:
            self.host_ids = host_ids
        else:
            self.host_ids += host_ids
        self.updated = datetime.utcnow()
        session.commit()
        session.close()
        return True
    

    def get_videos(self):
        session = SessionLocal()
        videos = []
        for host_id in self.host_ids:
            try:
                video_obj = session.query(Video).filter_by(host_id=host_id)
                for row in video_obj:
                    print(row)
            except:
                row = None
            if row is not None:
                 videos.append(row) 
        session.close()           
        return videos
    

    
