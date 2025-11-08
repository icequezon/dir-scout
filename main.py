import os

from src.logger import logger
from src.redis import get_redis_client, send_to_redis
from src.inotifywait_subprocess import InotifyWatcher


WATCH_DIR = os.getenv("WATCH_DIR", "/watched")
INCLUDE_DOTFILES = os.getenv("INCLUDE_DOTFILES", "false") == "true"


def main():
    logger.info("Starting...")
    watcher = InotifyWatcher(WATCH_DIR, INCLUDE_DOTFILES)
    watcher.start()
    redis_client = get_redis_client()

    for event in watcher.get_notifications():
        logger.info(f"Event: {event}")
        file_path = event["file_path"]
        action = event["action"]
        try:
            send_to_redis(redis_client, file_path, action)
        except Exception as e:
            logger.exception(e)


if __name__ == "__main__":
    main()
