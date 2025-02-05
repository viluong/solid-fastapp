from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str
    SECRET_KEY: str
    ALGORITHM_JWT: str
    ACCESS_TOKEN_EXPIRE_MINUTES: str
    PG_USER: str
    PG_HOST: str
    PG_DATABASE: str
    PG_PASSWORD: str
    PG_PORT: int
    REDIS_HOST: str
    REDIS_PORT: str

    class Config:
        env_file = ".env"

settings = Settings()