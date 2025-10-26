from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    postgres_url: str = "postgresql://postgres:password@localhost:5432/app"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # MinIO/S3
    minio_endpoint: str = "http://localhost:9000"
    minio_access_key: str = "minio"
    minio_secret_key: str = "minio123"
    s3_bucket_name: str = "designhire-media"

    # JWT
    jwt_secret: str = "changeme-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = True

    # Worker
    redis_queue_url: str = "redis://localhost:6379/1"

    # Stripe
    stripe_secret_key: str = ""
    stripe_publishable_key: str = ""

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
