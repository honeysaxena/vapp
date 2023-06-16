#from functools import lru_cache
from pydantic import BaseSettings, Field
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
print(BASE_DIR)

class Settings(BaseSettings):
    db_hostname: str 
    db_port: str
    db_password: str
    db_name: str 
    db_username: str 
    secret_key: str
    jwt_algorithm: str = Field(default='HS256')
    session_duration: int = Field(default=86400)
    template_dir: Path = Path(__file__).resolve().parent / 'templates'

    class Config:
        env_file = 'videoapp/.env'

settings = Settings()        


#@lru_cache
#def get_settings():
#    return Settings()       