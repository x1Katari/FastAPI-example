from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
  POSTGRES_DB: SecretStr
  POSTGRES_USER: SecretStr
  POSTGRES_PASSWORD: SecretStr
  POSTGRES_PORT: SecretStr
  POSTGRES_HOST: SecretStr


  class Config:
    env_file = '.env'
    env_file_encoding = 'utf-8'

config = Settings()
