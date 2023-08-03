from pathlib import Path

from pydantic import PostgresDsn, BaseSettings, Field
import os
from logging import config as logging_config

from .logger import LOGGING

logging_config.dictConfig(LOGGING)

PROJECT_HOST = os.getenv('PROJECT_HOST', '0.0.0.0')
PROJECT_PORT = int(os.getenv('PROJECT_PORT', '8000'))

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILES_FOLDER = Path(BASE_DIR, os.getenv('FILES_DIR', default='files'))


class AppSettings(BaseSettings):
    app_title: str = Field('ProjectName', env='PROJECT_NAME')
    database_dsn: PostgresDsn = Field(..., env='DATABASE_DSN')

    class Config:
        env_file = '.env'


app_settings = AppSettings()
