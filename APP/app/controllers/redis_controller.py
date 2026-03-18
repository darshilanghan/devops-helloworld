from flask import Blueprint, jsonify
from app.services.redis_service import redis_service

redis_bp = Blueprint("redis_data", __name__)

@redis_bp.route("/redis-data", methods=["GET"])
def redis_data():
    counter = redis_service.get_counter()
    all_keys = redis_service.get_all_keys()

    return jsonify({
        "global_visit_counter": counter,
        "redis_keys": all_keys,
    })
