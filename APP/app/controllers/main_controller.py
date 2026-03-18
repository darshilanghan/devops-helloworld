from flask import Blueprint, request, jsonify
from app.config.settings import settings
from app.services.visit_service import visit_service

main_bp = Blueprint("main", __name__)

def _get_client_ip() -> str:
    """Extract the real client IP, respecting proxy headers."""
    # X-Forwarded-For may contain a comma-separated list; take the first
    forwarded = request.headers.get("X-Forwarded-For", "")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.remote_addr or "unknown"


@main_bp.route("/", methods=["GET"])
def index():
    """GET / – main endpoint returning all required fields."""
    client_ip = _get_client_ip()
    user_agent = request.headers.get("User-Agent", "unknown")

    result = visit_service.process_visit(client_ip, user_agent)

    return jsonify({
        "message": "Hello World",
        "user_id": client_ip,
        "visit_count": result["visit_count"],
        "client_ip": result["client_ip"],
        "user_agent": result["user_agent"],
        "your_name": settings.AUTHOR_NAME,
        "timestamp": result["timestamp"],
    })
