# ============================================================
#  logger.py  —  Saves conversations to a log file
# ============================================================

import os
import datetime
from config import LOG_FILE, LOG_CONVERSATIONS


def log(role: str, text: str):
    """
    Log a conversation turn to file.
    role: "USER" or "MITRA"
    """
    if not LOG_CONVERSATIONS:
        return

    try:
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {role}: {text}\n")
    except Exception:
        pass  # Logging should never crash the app


def log_session_start():
    """Mark the beginning of a new session."""
    if not LOG_CONVERSATIONS:
        return
    try:
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"\n{'='*50}\n")
            f.write(f"SESSION: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"{'='*50}\n")
    except Exception:
        pass
