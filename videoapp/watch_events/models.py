import uuid
from sqlalchemy import Column, UUID, TIMESTAMP, String, Double, Boolean
from videoapp.database import Base
from videoapp.config import settings
from videoapp.database import SessionLocal


class WatchEvent(Base):
    __tablename__ = "watchevents"
    host_id = Column(String, primary_key=True)
    event_id = Column(UUID, primary_key=True, default=uuid.uuid1)
    user_id = Column(UUID, primary_key=True)
    path = Column(String)
    start_time = Column(Double)
    end_time = Column(Double)
    duration = Column(Double)
    complete = Column(Boolean, default=False)

    @property
    def completed(self):
        return (self.duration * 0.97) < self.end_time

    @staticmethod
    def get_resume_time(host_id, user_id):
        session = SessionLocal()
        resume_time = 0
        obj = session.query(WatchEvent).filter_by(host_id=host_id, user_id=user_id).first()
        if obj is not None:
            if not obj.complete or not obj.completed:
                resume_time = obj.end_time
        return resume_time        