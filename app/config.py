import os

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

MONGO_URI = os.getenv("MONGO_URI")

YOUR_NAME = os.getenv("YOUR_NAME", "Unknown")
USER_ID = os.getenv("USER_ID", "user")