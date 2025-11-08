import redis
import os

from src.logger import logger


REDIS_URL = os.getenv("REDIS_URL")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_STREAM = os.getenv("REDIS_STREAM", None)

REDIS_FULL_URL = f"redis://{REDIS_URL}:{REDIS_PORT}"


def get_redis_client():
    logger.info(f"Initializiing redis client with url: {REDIS_FULL_URL}")
    if not REDIS_URL or not REDIS_PORT:
        message = f"Failed to initialize redis client. Missing configuration: {REDIS_URL} : {REDIS_PORT}"
        logger.error(message)
        raise Exception(message)

    redis_client = redis.Redis.from_url(REDIS_FULL_URL)
    return redis_client


def send_to_redis(redis_client, file_path: str, action: str):
    logger.info(f"File event detected: {file_path}: {action}")

    if not REDIS_STREAM:
        message = "REDIS_STREAM is not defined"
        logger.error(message)
        raise Exception(message)

    message = {
        "file_path": file_path,
        "action": action,
    }
    message_id = redis_client.xadd(REDIS_STREAM, message)
    logger.info(f"Sent to Redis: {message} with message id: {message_id}")
