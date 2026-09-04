from pydantic_settings import BaseSettings


class Setting(BaseSettings):
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_KEY: str
    AWS_REGION: str
    S3_BUCKET_NAME: str

    class Config:
        env_file = ".env"


settings = Setting()  # type: ignore
