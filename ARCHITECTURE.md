# System Architecture

## Component Overview

| Component | Technology | Purpose |
|-----------|------------|---------|
| Claude AI | Anthropic API | Trading decisions |
| cTrader Bot | C# | Order execution |
| Orchestration | Python | Main loop, coordination |
| News Shield | Python + ForexFactory | News monitoring |
| Telegram | Bot API | Notifications |

## Data Flow

1. **M15 Bar Close** → C# writes market_data.json
2. **Python detects** → Calls Claude AI
3. **Claude returns** decision → Python writes signals.json
4. **C# reads** → Executes trade

## File-Based IPC

All communication is via JSON files in `C:\claude_bot\data\`:
- `market_data.json` - C# → Python (market state)
- `signals.json` - Python → C# (trading decisions)
- `account.json` - Account state