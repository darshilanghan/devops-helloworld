import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    APP_HOST: str = os.environ.get("APP_HOST", "0.0.0.0")
    APP_PORT: int = int(os.environ.get("APP_PORT", "5005"))
    APP_DEBUG: bool = os.environ.get("APP_DEBUG", "false").lower() == "true"
    APP_NAME: str = os.environ.get("APP_NAME", "HelloWorld App")

    AUTHOR_NAME: str = os.environ.get("AUTHOR_NAME", "Darsh Dobariya")

    # 🔥 FIXED HERE
    REDIS_HOST: str = os.environ.get("REDIS_HOST", "172.17.0.1")
    REDIS_PORT: int = int(os.environ.get("REDIS_PORT", "6379"))
    REDIS_DB: int = int(os.environ.get("REDIS_DB", "0"))
    REDIS_PASSWORD: str = os.environ.get("REDIS_PASSWORD", "")
    REDIS_COUNTER_KEY: str = os.environ.get("REDIS_COUNTER_KEY", "global:visit_counter")

    # 🔥 FIXED HERE
    MONGO_URI: str = os.environ.get("MONGO_URI", "mongodb://172.17.0.1:27017")
    MONGO_DB_NAME: str = os.environ.get("MONGO_DB_NAME", "helloworld_db")
    MONGO_COLLECTION: str = os.environ.get("MONGO_COLLECTION", "visits")

    @classmethod
    def redis_url(cls) -> str:
        if cls.REDIS_PASSWORD:
            return f"redis://:{cls.REDIS_PASSWORD}@{cls.REDIS_HOST}:{cls.REDIS_PORT}/{cls.REDIS_DB}"
        return f"redis://{cls.REDIS_HOST}:{cls.REDIS_PORT}/{cls.REDIS_DB}"


settings = Settings()