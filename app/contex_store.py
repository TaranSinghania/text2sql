# app/context_store.py

import redis
import json
import os
import logging

# Read Redis host and port from environment variables.
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
logging.info("Connecting to Redis at %s:%s", REDIS_HOST, REDIS_PORT)

# Configure the Redis client.
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)

def get_context(user_id: str):
    """Retrieve the conversation context for a given user_id from Redis."""
    try:
        data = redis_client.get(user_id)
        if data:
            return json.loads(data)
    except Exception as e:
        logging.error("Error retrieving context for user_id %s: %s", user_id, e)
    return []

def set_context(user_id: str, context):
    """Store the conversation context for a given user_id into Redis."""
    try:
        redis_client.set(user_id, json.dumps(context))
    except Exception as e:
        logging.error("Error setting context for user_id %s: %s", user_id, e)
