#import uuid
#import json
from typing import Optional
from pydantic import BaseModel, Field, validator


class VideoIndexSchema(BaseModel):
    objectID: str = Field(alias='host_id')
    objectType: str = "Video"    
    title: Optional[str]
    path: str = Field(alias='host_id')

    @validator("path")
    def set_path(cls, v, values, **kwargs):
        host_id = v
        return f"/videos/{host_id}"
    
