"""Application configuration"""
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings"""
    
    # App configuration
    APP_NAME: str = Field(default="JS Miner API", description="Application name")
    APP_VERSION: str = Field(default="2.0.0", description="Application version")
    DEBUG: bool = Field(default=True, description="Debug mode")
    HOST: str = Field(default="0.0.0.0", description="Host address")
    PORT: int = Field(default=8000, description="Port number")
    
    # Logging
    LOG_LEVEL: str = Field(default="INFO", description="Log level")
    VERBOSE_LOGGING: bool = Field(default=True, description="Enable verbose logging")
    
    # Scanner configuration
    MAX_WORKERS: int = Field(default=10, description="Maximum concurrent workers")
    MAX_RESPONSE_HIGHLIGHTS: int = Field(default=500, description="Max response highlights")
    SHANNON_ENTROPY_THRESHOLD: float = Field(default=3.5, description="Shannon entropy threshold")
    
    # NPM Registry
    NPM_REGISTRY_URL: str = Field(default="https://registry.npmjs.org", description="NPM registry URL")
    NPM_JS_URL: str = Field(default="https://www.npmjs.com", description="NPM JS URL")
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
