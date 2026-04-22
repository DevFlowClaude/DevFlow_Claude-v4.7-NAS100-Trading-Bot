"""
Dashboard Logger - Complete working version
"""

import json
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


class DashboardLogger:
    """Logs events for the dashboard."""
    
    def __init__(self, log_dir: Path):
        self.log_file = log_dir / "dashboard_log.json"
        self._buffer = []
        self._max_entries = 500
    
    def write(self, level: str, event_type: str, message: str):
        """Write a log entry."""
        try:
            self._buffer.append({
                "ts": datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
                "level": level,
                "event": event_type,
                "msg": str(message)[:300],
            })
            
            if len(self._buffer) > self._max_entries:
                self._buffer = self._buffer[-self._max_entries:]
            
            if level == "ERROR" or len(self._buffer) % 10 == 0:
                self.flush()
                
        except Exception as e:
            logger.debug(f"Log write error: {e}")
    
    def flush(self):
        """Flush buffer to file."""
        try:
            with open(self.log_file, 'w', encoding='utf-8') as f:
                json.dump(self._buffer, f, indent=2)
        except Exception as e:
            logger.debug(f"Flush error: {e}")