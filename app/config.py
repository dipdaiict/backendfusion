from typing import Optional
from pydantic import ConfigDict
from pydantic_settings import BaseSettings

class PostgresSettings(BaseSettings):
    postgres_hostname: str
    postgres_port: str
    postgres_password: str
    postgres_name: str
    postgres_username: str

    model_config = ConfigDict(env_file=".env", extra="ignore")

# Initialize the settings
postgres_settings = PostgresSettings()