import openai
import os
from os import path
from platform import system
from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    BASE_DIR: str = path.dirname((path.abspath(__file__))) # 기본 디렉토리 위치
    # 개발할때 로컬에서 확인
    LOCAL_MODE: bool = True if system().lower().startswith("darwin") or system().lower().startswith("Windows") else False
    app_name: str = "Imizi API"
    TEST_MODE: bool = False
    # 어떤 프론트엔드에서 접속을 허용할거냐
    ALLOW_SITE = ["*"]
    # 해당 서버가 해당 도메인으로 접속
    TRUSTED_HOSTS = ["*"]
    JWT_ALGORITHM = "HS256"
    JWT_SECRET_KEY = os.getenv("JWT_SECRET", "imizi-secret")
    ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 1  # one day
    api_key = ""
    client_id = ""
    client_secret = ""
# 3가지 셋팅
class DevSettings(Settings):
    DB_URL = "mysql+pymysql://root:wlstjd@localhost:3306/sqlalchemy?charset=utf8mb4"


class TestSettings(Settings):
    DB_URL = "mysql+pymysql://root:wlstjd@localhost:3306/imizi?charset=utf8mb4"


class ProdSettings(Settings):
    DB_URL = "mysql+pymysql://root:wlstjd@localhost:3306/imizi?charset=utf8mb4"


def get_env():
    cfg_cls = dict(
        prd=ProdSettings,
        dev=DevSettings,
        test=TestSettings,
    )
    env = cfg_cls[os.getenv("FASTAPI_ENV", "dev")]()

    return env


settings = get_env()
