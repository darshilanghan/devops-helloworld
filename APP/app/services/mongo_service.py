from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from app.config.settings import settings
from app.models.visit_model import VisitModel

class MongoService:
    def __init__(self):
        self._client: MongoClient | None = None
        self._db: Database | None = None
        self._collection: Collection | None = None

    def connect(self) -> None:
        """Establish MongoDB connection."""
        self._client = MongoClient(settings.MONGO_URI)
        self._db = self._client[settings.MONGO_DB_NAME]
        self._collection = self._db[settings.MONGO_COLLECTION]

    @property
    def collection(self) -> Collection:
        if self._collection is None:
            self.connect()
        return self._collection

    # CRUD

    def store_visit(self, visit: VisitModel) -> str:
        """Insert a visit document and return its inserted id."""
        result = self.collection.insert_one(visit.to_dict())
        return str(result.inserted_id)

    def get_all_visits(self, limit: int = 100) -> list[dict]:
        """Return the most recent visits."""
        cursor = self.collection.find(
            {}, {"_id": 0}
        ).sort("timestamp", -1).limit(limit)
        return list(cursor)

    # health

    def ping(self) -> bool:
        """Return True if MongoDB is reachable."""
        try:
            self._client_instance.admin.command("ping")
            return True
        except Exception:
            return False

    @property
    def _client_instance(self) -> MongoClient:
        if self._client is None:
            self.connect()
        return self._client


# Singleton instance shared across the app
mongo_service = MongoService()
