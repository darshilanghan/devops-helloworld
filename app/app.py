from flask import Flask, request, jsonify
import redis
from pymongo import MongoClient
import os

app = Flask(__name__)

# Runtime configs
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017")

NAME = "Darshil"

# Redis connection
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

# Mongo connection
mongo_client = MongoClient(MONGO_URI)
db = mongo_client["hello_db"]
collection = db["visits"]

@app.route("/")
def home():

    counter = r.incr("global_counter")

    ip = request.remote_addr
    agent = request.headers.get("User-Agent")

    collection.insert_one({
        "ip": ip,
        "counter": counter
    })

    return jsonify({
        "message": "Hello World",
        "user_id": counter,
        "visit_count": counter,
        "client_ip": ip,
        "user_agent": agent,
        "name": NAME
    })


@app.route("/health")
def health():
    return "OK", 200


@app.route("/redis-data")
def redis_data():
    keys = r.keys("*")

    data = {}
    for k in keys:
        data[k] = r.get(k)

    return jsonify(data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)