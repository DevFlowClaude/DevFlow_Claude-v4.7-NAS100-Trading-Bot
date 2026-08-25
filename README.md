# 🤖 Claude AI NAS100 Trading Bot

[![License: Proprietary](https://img.shields.io/badge/License-Proprietary-red.svg)](LICENSE)

# DevFlow_Claude v4.7 (NAS100) Trading Bot

## 🚀 System Overview
This is an M15 NAS100 trading system that uses Claude AI for decision-making.

The architecture:
- C# cBot collects market data
- Python processes data and calls Claude AI
- cBot executes trades based on AI signals

---

## ⚙️ Workflow

1. On every M15 candle close, the cBot writes to `market_data.json`:
   - EMA, RSI, ATR, VWAP indicators
   - current positions

2. Python script:
   - reads market data
   - sends it to Claude AI

3. Claude AI:
   - analyzes the last 20 candles
   - generates a decision: **BUY / SELL / WAIT**

4. The decision is saved to `signals.json`

5. The cBot:
   - executes market or limit orders
   - applies SL/TP rules

---

## 📊 Key Features

- M15 timeframe analysis  
- Last 20 candles context evaluation  
- Indicators:
  - EMA20 / EMA50 / EMA200  
  - RSI  
  - ATR  
  - VWAP  
- Daily high/low tracking  
- News filter (ForexFactory, high-impact USD events)  
- Pre-news safety:
  - positions closed 10 minutes before events  
  - trading paused during high impact news  
- Telegram notifications  
- Chart overlay:
  - SL/TP levels  
  - entry zones  

---

## 🛡️ Risk Management

- Fixed risk per trade: **1%**  
- Daily loss limit: **5%**  
- Max drawdown: **10%**  
- SL range: **10–50 points**  
- Minimum RR ratio: **1.5:1**

---

## 🧠 Tech Stack

- C# (cTrader cBot)  
- Python 3.10+  
- Claude API (Anthropic)  
- ForexFactory data  
- Telegram Bot API  
- JSON communication layer  

---

## 🏦 Prop Firm Compatibility

Designed for prop firm environments such as FundingPips-style challenges.

Key compliance logic:
- strict drawdown control  
- daily loss protection  
- fixed risk model (~1%)  
- news-time trading restrictions  

---

## 🔒 System Design Philosophy

The public version demonstrates:
- architecture  
- data flow  
- indicator usage  
- system structure  

The edge of the system comes from:
- AI decision logic  
- optimized parameters  
- execution and risk management layer  

These are not included in the public repo.

---

## 📦 What is included

- Full C# cBot implementation  
- Python AI bridge system  
- JSON communication structure  
- Config templates  
- Documentation  
- Setup guide (basic)

---

## 🧪 Access Model

No free demo is provided.

Trial access is available for **50 USD**, allowing:
- live environment execution  
- real-time signal observation  
- system evaluation before full access  

---

## ⚠️ Disclaimer

- Not financial advice  
- Trading involves risk  
- No guaranteed returns  

---

## 🧾 Summary

The public repo shows that the system is **technically built and functional in structure**.  
The full version contains the optimized logic used in real execution environments.


---

## @DevFlow_Claude

Expert Python & C# Developer | AI Systems & Automation

Specialized in building:
- high-performance trading bots 🤖  
- autonomous AI agents 🧠  
- complex process automation systems  

I also provide multilingual solutions 🌍:
- subtitles & dubbing scripts 📝  
- short-form & long-form video localization 🎥  
- culturally adapted content for global markets 🎨  

Using cutting-edge technologies 🛠️, I deliver:
- stable and scalable systems  
- high-quality, tailored solutions  
- fast turnaround times ⏱️  

🌐 Languages:
🇬🇧 English | 🇩🇪 German | 🇭🇺 Hungarian | 🇫🇷 French | 🇮🇹 Italian | 🇷🇺 Russian  

---

## 📩 Contact  
Linktree: [https://linktr.ee/DevFlow_C](https://linktr.ee/DevFlow_C)
