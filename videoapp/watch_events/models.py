import uuid
from sqlalchemy import Column, UUID, TIMESTAMP, String, Double, Boolean
from videoapp.database import Base
from videoapp.config import settings


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