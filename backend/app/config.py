"""Settings loaded from environment variables (see .env.example for the names)."""
import secrets
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "sqlite:///./township.db"

    
    jwt_secret: str = ""
    jwt_hours: int = 12

    otp_mock: bool = True
    demo_otp: str = "" 
    otp_max_attempts: int = 5
    otp_window_minutes: int = 10


    rate_per_sqft_paise: int = 650
    late_fee_annual_percent: float = 18.0
    late_fee_grace_days: int = 0  

    frontend_origin: str = "http://localhost:5173"
    upload_dir: str = "uploads"
    max_upload_bytes: int = 3 * 1024 * 1024


@lru_cache
def get_settings() -> Settings:
    s = Settings()
    if not s.jwt_secret:
        s.jwt_secret = secrets.token_urlsafe(48)
    if s.otp_mock and not s.demo_otp:
        s.demo_otp = "".join(secrets.choice("0123456789") for _ in range(6))
    return s