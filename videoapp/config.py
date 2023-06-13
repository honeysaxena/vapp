#from functools import lru_cache
from pydantic import BaseSettings, Field
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
print(BASE_DIR)

class Settings(BaseSettings):
    db_hostname: str = Field(..., env='DB_HOSTNAME')
    db_port: int = Field(..., env='DB_PORT') 
    db_password: str = Field(..., env='DB_PASSWORD')
    db_name: str = Field(..., env='DB_NAME')
    db_username: str = Field(..., env='DB_USERNAME')
    template_dir: Path = Path(__file__).resolve().parent / 'templates'

    class Config:
        env_file = '.env'

settings = Settings()        


#@lru_cache
#def get_settings():
#    return Settings()       