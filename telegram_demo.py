"""
Telegram Bot - Complete working version (no secrets)
"""

import httpx
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class TelegramBot:
    """Telegram notification sender."""
    
    def __init__(self, token: str, chat_id: str):
        self.token = token
        self.chat_id = chat_id
        self._client = None
    
    async def send(self, text: str, parse_mode: str = "HTML") -> bool:
        """Send message to Telegram."""
        if not self.token or not self.chat_id:
            logger.debug("Telegram not configured")
            return False
        
        try:
            url = f"https://api.telegram.org/bot{self.token}/sendMessage"
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.post(url, json={
                    "chat_id": self.chat_id,
                    "text": text,
                    "parse_mode": parse_mode,
                })
                return resp.status_code == 200
        except Exception as e:
            logger.debug(f"Telegram error: {e}")
            return False
    
    async def send_trade_open(self, pair: str, side: str, entry: float, sl: float, tp: float):
        """Send trade opened notification."""
        text = f"<b>TRADE OPENED - {side}</b>\n{pair}\nEntry: {entry}\nSL: {sl}\nTP: {tp}"
        await self.send(text)
    
    async def send_trade_close(self, pair: str, profit: float, reason: str = ""):
        """Send trade closed notification."""
        result = "PROFIT" if profit >= 0 else "LOSS"
        text = f"<b>TRADE CLOSED - {result}</b>\n{pair}\nP&L: ${profit:+.2f}"
        if reason:
            text += f"\nReason: {reason}"
        await self.send(text)
    
    async def send_news_pause(self, label: str):
        """Send news pause alert."""
        text = f"<b>NEWS PAUSE</b>\nTrading paused\n{label}\nWindow: +/-10 min"
        await self.send(text)
    
    async def send_news_resume(self):
        """Send news resume notification."""
        await self.send("<b>NEWS PAUSE ENDED</b>\nTrading resumed")