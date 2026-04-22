# Trading Strategy - NAS100 M15

## Core Rules

1. **Trend following** - only trade in direction of EMA200
2. **News awareness** - no trading ±10 min around High impact USD news
3. **Session hours** - only 08:30-21:00 CET (US market)

## Entry Conditions

### BUY
- Price > EMA200
- Price > VWAP
- Bullish candle close
- RSI > 40

### SELL
- Price < EMA200
- Price < VWAP
- Bearish candle close
- RSI < 60

## Stop Loss

- Minimum: 10 points
- Maximum: 50 points
- Below swing low (BUY) / Above swing high (SELL)

## Take Profit

- Minimum 1.5:1 ratio
- Typical 2:1 or 3:1