from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")
    groq_api_key: str = ""
    groq_base_url: str = "https://api.groq.com/openai/v1"
    llm_model: str = "openai/gpt-oss-20b"
    tavily_api_key: str = ""
    agent_max_steps: int = 6
    agent_temperature: float = 0.2
    request_timeout_seconds: int = 60
    sqlite_path: str = "./data/agent.db"

    def prepare(self):
        Path(self.sqlite_path).parent.mkdir(parents=True, exist_ok=True)

@lru_cache
def get_settings():
    return Settings()
