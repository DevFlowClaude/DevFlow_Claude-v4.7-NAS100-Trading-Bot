"""
Claude AI Integration - DEMO VERSION
Full implementation (system prompt, trading logic) is proprietary.
This shows the integration pattern only.
"""

import json
import asyncio
import logging
from typing import Optional, Dict

logger = logging.getLogger('DevFlowClaude')
ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"

# These values would come from config in production
CLAUDE_MIN_CONFIDENCE = 70
CLAUDE_SL_MIN_POINTS = 10
CLAUDE_SL_MAX_POINTS = 50


class ClaudeAI:
    """Claude API integration for NAS100 trading decisions."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self._client = None
        logger.info("ClaudeAI demo initialized")
    
    async def analyze_and_decide(self, market_data: dict) -> Optional[dict]:
        """
        Analyze market data and return trading decision.
        
        Args:
            market_data: Contains bars, indicators, positions
            
        Returns:
            Decision dict with action, sl_price, tp_price, confidence
        """
        if not self.api_key:
            logger.error("API key missing")
            return None
        
        # Build prompt from market data (full prompt proprietary)
        prompt = self._build_prompt(market_data)
        
        # Call Claude API
        decision = await self._call_claude(prompt)
        
        if decision:
            decision = self._validate_decision(decision)
            logger.info(f"Decision: {decision.get('action')} @ {decision.get('confidence')}%")
        
        return decision
    
    def _build_prompt(self, data: dict) -> str:
        """
        PROMPT STRUCTURE (actual 2000-token prompt is proprietary):
        
        1. System prompt: Trading rules, NAS100 instrument specs, SL/TP rules
        2. User prompt: Current market data, indicators, positions
        3. Output format: JSON schema
        
        The complete prompt contains the core trading strategy
        and is not included in this demo.
        """
        # Simplified demo prompt
        bars = data.get("bars", [])
        return f"""
        Analyze NAS100 M15 data.
        Current price: {data.get('current_price', 0)}
        RSI: {data.get('rsi', 0)}
        Decision must be JSON: {{"action": "BUY/SELL/WAIT", "sl_price": 0, "tp_price": 0, "confidence": 0}}
        """
    
    async def _call_claude(self, prompt: str) -> Optional[dict]:
        """Call Claude API with retry logic."""
        # Full implementation includes:
        # - HTTP POST with headers
        # - Retry logic (3 attempts, 5s delay)
        # - Response parsing
        # - JSON extraction from markdown code blocks
        return None  # Demo placeholder
    
    def _validate_decision(self, decision: dict) -> dict:
        """Validate and sanitize decision."""
        valid_actions = {"BUY", "SELL", "CLOSE", "WAIT"}
        action = decision.get("action", "WAIT")
        if action not in valid_actions:
            action = "WAIT"
        
        confidence = max(0, min(100, decision.get("confidence", 0)))
        
        if action in ("BUY", "SELL") and confidence < CLAUDE_MIN_CONFIDENCE:
            action = "WAIT"
        
        sl = max(CLAUDE_SL_MIN_POINTS, min(CLAUDE_SL_MAX_POINTS, decision.get("sl_price", 0)))
        
        return {
            "action": action,
            "sl_price": sl,
            "tp_price": decision.get("tp_price", 0),
            "confidence": confidence,
            "reasoning": decision.get("reasoning", "")[:200],
        }
    
    async def close(self):
        """Close HTTP client."""
        if self._client:
            await self._client.aclose()