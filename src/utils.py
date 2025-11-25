import json
import time
import logging
import functools
from datetime import datetime
from typing import Callable, Any


# -------------------------------------------------------------------
# Logging Setup (JSON formatted logs)
# -------------------------------------------------------------------

def setup_logging(level=logging.INFO):
    logging.basicConfig(
        level=level,
        format='{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}'
    )
    logging.info("Logging initialized.")


# -------------------------------------------------------------------
# Exponential Backoff Retry Decorator
# -------------------------------------------------------------------

def retry_with_backoff(retries=5, backoff_factor=1.5, exceptions=(Exception,)):
    def decorator(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            attempt = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempt += 1
                    if attempt > retries:
                        logging.error(f"{func.__name__} failed after {retries} retries: {e}")
                        raise
                    sleep_time = (backoff_factor ** attempt)
                    logging.warning(f"{func.__name__} failed: {e}, retrying in {sleep_time:.2f}s...")
                    time.sleep(sleep_time)
        return wrapped
    return decorator


# -------------------------------------------------------------------
# Rate Limiting Decorator (simple: requests per second)
# -------------------------------------------------------------------

def rate_limit(max_calls_per_sec: float):
    min_interval = 1.0 / max_calls_per_sec
    def decorator(func):
        last_call = [0.0]
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            elapsed = time.time() - last_call[0]
            sleep_for = min_interval - elapsed
            if sleep_for > 0:
                time.sleep(sleep_for)
            last_call[0] = time.time()
            return func(*args, **kwargs)
        return wrapped
    return decorator


# -------------------------------------------------------------------
# JSON Utilities
# -------------------------------------------------------------------

def write_jsonl(file_path: str, data: dict):
    """Append a dict as JSON to a JSONL file."""
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")


def safe_json_dumps(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, default=str)


# -------------------------------------------------------------------
# Timestamp Helpers
# -------------------------------------------------------------------

def now_iso():
    """Return UTC timestamp."""
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
