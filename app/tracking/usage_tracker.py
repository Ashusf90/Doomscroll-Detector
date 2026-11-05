import time
import json
from pathlib import Path
from datetime import datetime

HISTORY_FILE = Path("data/usage_history.json")


class UsageTracker:
    def __init__(self):
        self.session_start = None
        self.total_seconds = 0
        self.sessions = 0
        self.history = []
        self._load_history()

    def _load_history(self):
        HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)

        if HISTORY_FILE.exists():
            try:
                self.history = json.loads(HISTORY_FILE.read_text())
            except (json.JSONDecodeError, OSError):
                self.history = []

    def _save_history(self):
        HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
        HISTORY_FILE.write_text(json.dumps(self.history, indent=2))

    def update(self, detected):
        now = time.time()

        if detected and self.session_start is None:
            self.session_start = now
            self.sessions += 1

        elif not detected and self.session_start is not None:
            duration = now - self.session_start

            self.total_seconds += duration
            self.history.append({
                "date": datetime.now().strftime("%Y-%m-%d"),
                "start": datetime.fromtimestamp(
                    self.session_start
                ).strftime("%H:%M:%S"),
                "duration": round(duration, 1)
            })

            self._save_history()
            self.session_start = None

        current = self.total_seconds
        if self.session_start is not None:
            current += now - self.session_start

        return int(current)

    def get_total(self):
        current = self.total_seconds

        if self.session_start is not None:
            current += time.time() - self.session_start

        return int(current)

    def get_sessions(self):
        return self.sessions

    def get_history(self):
        return self.history

    def reset(self):
        self.session_start = None
        self.total_seconds = 0
        self.sessions = 0
        self.history = []
        self._save_history()
