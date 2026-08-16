from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    llm_enabled: bool = False
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    openai_base_url: str = "https://api.openai.com/v1"
    cors_origins: str = "http://localhost:5173"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
