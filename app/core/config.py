from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # 数据库
    DATABASE_URL: str

    # 模型
    EMBEDDING_MODEL: str

    # chroma
    CHROMA_PERSIST_DIR: str
    CHROMA_COLLECTION_NAME: str

    class Config:
        env_file = ".env"

settings = Settings()