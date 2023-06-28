from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from videoapp.watch_events.schemas import WatchEventSchema
from videoapp.watch_events.models import WatchEvent
from videoapp.database import SessionLocal

router = APIRouter()

@router.post("/api/events/watch", response_model=WatchEventSchema)
def watch_event_view(request: Request, watch_event:WatchEventSchema):   
    if (request.user.is_authenticated):
        cleaned_data = watch_event.dict()
        data = cleaned_data.copy()
        data.update({
            "user_id": request.user.username
        })  
        session = SessionLocal()
        eventobj1 = WatchEvent(**data)
        session.add(eventobj1)
        session.commit()
        session.refresh(eventobj1)
        session.close()
        return watch_event

    return watch_event
