import uuid
from pydantic import BaseModel
from pydantic import (
    BaseModel,
    validator,
    root_validator
)
from videoapp.videos.extractors import extract_video_id
from videoapp.videos.models import Video

from videoapp.playlists.models import Playlists
from videoapp.database import SessionLocal



class PlaylistsCreateSchema(BaseModel):
    title: str
    user_id: str


    

class PlaylistVideoAddSchema(BaseModel):
    url: str
    title: str
    user_id: str
    playlist_id: uuid.UUID

    @validator("url")
    def validate_youtube_url(cls, v, values, **kwargs):
        url = v
        video_id = extract_video_id(url)
        if video_id is None:
            raise ValueError(f"{url} is not a valid YouTube URL")
        return url

    @validator("playlist_id")
    def validate_playlist_id(cls, v, values, **kwargs):
        session = SessionLocal()
        q = session.query(Playlists).filter_by(db_id=v)

        if q.count() == 0:
            raise ValueError(f"{v} is not a valid playlist.")
        session.close()
        return v

    @root_validator
    def validate_data(cls, values):
        session = SessionLocal()
        url = values.get('url')
        title = values.get('title')
        playlist_id = values.get('playlist_id')
        if url is None:
            raise ValueError("A valid URL is required.")
        user_id = values.get('user_id')
        video_obj = None
        extra_data = {}
        if title is not None:
            extra_data['title'] = title
        try:
            video_obj, created = Video.get_or_create(url, user_id=user_id, **extra_data)  
        except:
            raise ValueError("There is a problem with your request, Please try again.")
        if not isinstance(video_obj, Video):
            raise ValueError("There is a problem with your account, please try again.")
        if playlist_id:
            
            playlist_obj = session.query(Playlists).filter_by(db_id=playlist_id)
            for obj in playlist_obj:
                obj.add_host_ids(host_ids=[video_obj.host_id])
                
            session.add(obj)
            session.commit()
            session.refresh(obj)

            session.close()   
        
        return video_obj.as_data()
    

