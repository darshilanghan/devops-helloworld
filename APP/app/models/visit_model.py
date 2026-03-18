from datetime import datetime, timezone


class VisitModel:
    def __init__(self, client_ip: str, visit_count: int, user_agent: str = ""):
        self.client_ip = client_ip
        self.visit_count = visit_count
        self.user_agent = user_agent
        self.timestamp = datetime.now(timezone.utc)

    def to_dict(self) -> dict:
        return {
            "client_ip": self.client_ip,
            "visit_count": self.visit_count,
            "user_agent": self.user_agent,
            "timestamp": self.timestamp,
        }

    @staticmethod
    def from_dict(data: dict) -> "VisitModel":
        """Deserialise a MongoDB document into a VisitModel."""
        model = VisitModel(
            client_ip=data.get("client_ip", ""),
            visit_count=data.get("visit_count", 0),
            user_agent=data.get("user_agent", ""),
        )
        model.timestamp = data.get("timestamp", datetime.now(timezone.utc))
        return model

    def __repr__(self) -> str:
        return (
            f"<VisitModel ip={self.client_ip} count={self.visit_count} "
            f"ua={self.user_agent} ts={self.timestamp}>"
        )
