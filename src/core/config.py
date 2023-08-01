from pathlib import Path

from pydantic import PostgresDsn, BaseSettings
import os
from logging import config as logging_config

from .logger import LOGGING

logging_config.dictConfig(LOGGING)

PROJECT_NAME = os.getenv('PROJECT_NAME', 'library')
PROJECT_HOST = os.getenv('PROJECT_HOST', '0.0.0.0')
PROJECT_PORT = int(os.getenv('PROJECT_PORT', '8000'))
DATABASE_DSN = os.getenv('DATABASE_DSN')

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILES_FOLDER = Path(BASE_DIR, os.getenv('FILES_DIR', default='files'))


class AppSettings(BaseSettings):
    app_title: str = PROJECT_NAME
    database_dsn: PostgresDsn = DATABASE_DSN

    class Config:
        env_file = '.env'


app_settings = AppSettings()
