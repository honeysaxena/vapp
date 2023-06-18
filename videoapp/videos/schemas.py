from pydantic import (
    BaseModel,
    validator,
    root_validator
)
from videoapp.videos.extractors import extract_video_id
from videoapp.users.exceptions import InvalidUserIDException
from videoapp.videos.exceptions import InvalidYoutubeVideoURLException, VideoAlreadyAddedException
from videoapp.videos.models import Video


class VideoCreateSchema(BaseModel):
    url: str
    user_id: str

    @validator("url")
    def validate_youtube_url(cls, v, values, **kwargs):
        url = v
        video_id = extract_video_id(url)
        if video_id is None:
            raise ValueError(f"{url} is not a valid YouTube URL")
        return url


    @root_validator
    def validate_data(cls, values):
        url = values.get('url')
        user_id = values.get('user_id')
        video_obj = None
        try:
            video_obj = Video.add_video(url, user_id=user_id)
        except InvalidYoutubeVideoURLException:
            raise ValueError(f"{url} is not a valid YouTube URL")
        except VideoAlreadyAddedException:
            raise ValueError(f"{url} has already been added to your account.")
        except InvalidUserIDException:
            raise ValueError("There is a problem with your account, Please try again.")    
        except:
            raise ValueError("There is a problem with your account, Please try again.")
        if  video_obj is None:
            raise ValueError("There is a problem with your account, Please try again.")
        if not isinstance(video_obj, Video):
            raise ValueError("There is a problem with your account, please try again.")
        return video_obj.as_data()
    

