from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "TradeForge"
    environment: str = "development"
    log_level: str = "INFO"
    default_capital: float = 10000.0
    default_risk_percent: float = 1.0
    max_open_positions: int = 3

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
