"""
News Monitor - ForexFactory Calendar
Simplified version showing the pattern.
"""

import httpx
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import logging

logger = logging.getLogger(__name__)


class NewsMonitor:
    """
    Monitors High impact USD events from ForexFactory.
    """
    
    CALENDAR_URL = "https://nfs.faireconomy.media/ff_calendar_thisweek.json"
    PAUSE_MINUTES = 10  # Pause 10 min before/after
    
    def __init__(self):
        self.events: List[Dict] = []
        self._last_update = None
    
    def fetch_events(self) -> List[Dict]:
        """Fetch calendar and filter High impact USD events."""
        try:
            with httpx.Client(timeout=15.0) as client:
                response = client.get(self.CALENDAR_URL)
            
            if response.status_code != 200:
                logger.error(f"HTTP {response.status_code}")
                return []
            
            data = response.json()
            events = []
            
            for item in data:
                # Only High impact USD events
                if item.get("impact") != "High":
                    continue
                if item.get("country") != "USD":
                    continue
                
                events.append({
                    "title": item.get("title", "Unknown"),
                    "currency": "USD",
                    "impact": "High",
                    # Time parsing simplified - production handles timezones
                })
            
            self.events = events
            self._last_update = datetime.now()
            logger.info(f"Fetched {len(events)} High impact USD events")
            return events
            
        except Exception as e:
            logger.error(f"Fetch error: {e}")
            return []
    
    def check_status(self) -> Tuple[bool, bool, str]:
        """
        Check if trading should pause due to news.
        
        Returns:
            is_paused: bool - True if within PAUSE_MINUTES of news
            should_close: bool - True if news is about to start
            label: str - Event description
        """
        # Simplified - production compares actual timestamps
        return False, False, ""
    
    def get_upcoming(self, hours: int = 8) -> List[Dict]:
        """Get upcoming events within next X hours."""
        # Simplified version
        return self.events[:5]