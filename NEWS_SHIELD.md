# News Shield

## Critical Events for NAS100

| Event | Impact |
|-------|--------|
| FOMC Rate Decision | 🔴 Extreme |
| Non-Farm Payrolls | 🔴 Extreme |
| CPI / PCE | 🔴 Extreme |
| Fed Chair Speech | 🟡 High |
| Retail Sales | 🟡 High |

## Protection Logic

- **-10 min before**: Close positions, block new entries
- **During event**: Trading paused
- **+10 min after**: Block new entries only

## Implementation

The News Shield runs in Python, fetches ForexFactory calendar every 4 hours, and writes status to signals.json for the C# bot to read.