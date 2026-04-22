"""
Main Bot Orchestration - DEMO VERSION
Shows the loop structure and component integration.
"""

import asyncio
import logging
from datetime import datetime
from typing import Optional

logger = logging.getLogger('DevFlowClaude')

# Session hours (CET)
SESSION_START_HOUR = 8
SESSION_START_MIN = 30
SESSION_END_HOUR = 21
SESSION_END_MIN = 0

# Check interval (seconds)
M15_CHECK_INTERVAL = 10


def is_session_open(now: datetime) -> bool:
    """Check if trading session is open (weekdays 08:30-21:00 CET)."""
    if now.weekday() >= 5:  # Weekend
        return False
    
    current_minutes = now.hour * 60 + now.minute
    start_minutes = SESSION_START_HOUR * 60 + SESSION_START_MIN
    end_minutes = SESSION_END_HOUR * 60 + SESSION_END_MIN
    
    return start_minutes <= current_minutes < end_minutes


def current_m15_bar(now: datetime) -> datetime:
    """Return the start time of current M15 candle."""
    minute = (now.minute // 15) * 15
    return now.replace(minute=minute, second=0, microsecond=0)


class DevFlowBot:
    """Main bot orchestrator."""
    
    def __init__(self):
        self._running = True
        self._last_m15_bar = None
        self._session_was_open = None
        logger.info("DevFlowBot demo initialized")
    
    async def start(self):
        """Start the main loop."""
        logger.info("Main loop starting...")
        await self._run_loop()
    
    async def _run_loop(self):
        """Main orchestration loop."""
        while self._running:
            try:
                now = datetime.now()
                session_open = is_session_open(now)
                
                # Session state tracking
                if session_open != self._session_was_open:
                    if session_open:
                        logger.info("Session opened")
                    else:
                        logger.info("Session closed")
                    self._session_was_open = session_open
                
                # M15 bar detection
                if session_open:
                    await self._check_m15_bar(now)
                
                await asyncio.sleep(M15_CHECK_INTERVAL)
                
            except KeyboardInterrupt:
                self._running = False
            except Exception as e:
                logger.error(f"Loop error: {e}")
                await asyncio.sleep(10)
        
        logger.info("Bot stopped")
    
    async def _check_m15_bar(self, now: datetime):
        """Detect new M15 candle and trigger analysis."""
        current_bar = current_m15_bar(now)
        
        if self._last_m15_bar is None:
            self._last_m15_bar = current_bar
            return
        
        if current_bar > self._last_m15_bar:
            self._last_m15_bar = current_bar
            logger.info(f"New M15 candle: {current_bar.strftime('%H:%M')}")
            
            # In production: call Claude AI here
            # decision = await self.claude.analyze_and_decide(market_data)
            
            logger.info("Analysis triggered (Claude call would happen here)")
    
    async def stop(self):
        """Graceful shutdown."""
        self._running = False


if __name__ == "__main__":
    bot = DevFlowBot()
    try:
        asyncio.run(bot.start())
    except KeyboardInterrupt:
        logger.info("Stopped by user")