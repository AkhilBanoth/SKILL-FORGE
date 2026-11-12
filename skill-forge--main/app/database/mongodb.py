from pymongo import MongoClient
from app.config import settings

client = MongoClient(
    settings.MONGO_URL,
    serverSelectionTimeoutMS=5000,
)

database = client[settings.MONGO_DATABASE]

def check_mongodb() -> bool:
    try:
        client.admin.command("ping")
        return True
    except Exception:
        return False

def close_mongodb() -> None:
    client.close()

