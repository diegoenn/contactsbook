import os
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer

load_dotenv(dotenv_path='ContactBook/.env')


class Settings:
    JWT_SECRET = os.getenv('JWT_SECRET')
    TOKEN_URL = OAuth2PasswordBearer(tokenUrl=os.getenv('TOKEN_URL'))
    ALGORITHMS = os.getenv('ALGORITHMS')


settings = Settings()


