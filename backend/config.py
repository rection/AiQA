from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DEEPSEEK_API_KEY: str = ""
    DEEPSEEK_BASE_URL: str = "https://api.deepseek.com"
    DEEPSEEK_MODEL: str = "deepseek-chat"
    DEEPSEEK_EMBEDDING_MODEL: str = "deepseek-embedding"
    TAVILY_API_KEY: str = ""
    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: int = 3306
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = ""
    MYSQL_DATABASE: str = "ai_assistant"
    CHROMA_PERSIST_DIR: str = "./chroma_data"
    UPLOAD_DIR: str = "./uploads"
    MAX_FILE_SIZE: int = 50 * 1024 * 1024
    MAX_TOOL_CALLS: int = 5
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 50
    APP_VERSION: str = "1.0.0"
    CORS_ORIGINS: list[str] = ["http://localhost:5173"]

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
