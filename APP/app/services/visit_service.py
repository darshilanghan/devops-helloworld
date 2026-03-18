from app.models.visit_model import VisitModel
from app.services.redis_service import redis_service
from app.services.mongo_service import mongo_service


class VisitService:
    @staticmethod
    def process_visit(client_ip: str, user_agent: str) -> dict:
        visit_count = redis_service.increment_counter()

        visit = VisitModel(
            client_ip=client_ip,
            visit_count=visit_count,
            user_agent=user_agent,
        )

        mongo_service.store_visit(visit)

        return {
            "visit_count": visit_count,
            "client_ip": client_ip,
            "user_agent": user_agent,
            "timestamp": visit.timestamp.isoformat(),
        }


visit_service = VisitService()
