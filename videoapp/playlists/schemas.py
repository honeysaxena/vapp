#import uuid
from pydantic import BaseModel

#from videoapp.playlists.models import Playlists
#from playlistapp.database import SessionLocal

class PlaylistsCreateSchema(BaseModel):
    title: str
    user_id: str


    

