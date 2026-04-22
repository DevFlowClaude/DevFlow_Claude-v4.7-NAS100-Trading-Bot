/**
 * Claude AI NAS100 Bot - DEMO VERSION
 * Full implementation (volume calculation, SL validation, symbol detection) is proprietary.
 * This shows the structure and integration pattern.
 */

using cAlgo.API;
using System;
using System.IO;
using System.Text;
using System.Text.Json;

namespace cAlgo.Robots
{
    [Robot(TimeZone = TimeZones.CentralEuropeanStandardTime)]
    public class ClaudeBotDemo : Robot
    {
        // Parameters
        [Parameter("Data Directory", DefaultValue = @"C:\claude_bot\data")]
        public string DataDir { get; set; }
        
        [Parameter("Risk Per Trade Pct", DefaultValue = 1.0)]
        public double RiskPerTradePct { get; set; }
        
        [Parameter("SL Min Points", DefaultValue = 10)]
        public int SlMinPoints { get; set; }
        
        [Parameter("SL Max Points", DefaultValue = 50)]
        public int SlMaxPoints { get; set; }
        
        // File paths
        private string _marketDataFile;
        private string _signalsFile;
        
        // State
        private DateTime _lastSignalRead;
        private SignalsData _lastSignal;
        
        protected override void OnStart()
        {
            Directory.CreateDirectory(DataDir);
            _marketDataFile = Path.Combine(DataDir, "market_data.json");
            _signalsFile = Path.Combine(DataDir, "signals.json");
            
            Print("Claude Bot Demo started on " + SymbolName);
            Print("SL range: {0}-{1} points", SlMinPoints, SlMaxPoints);
        }
        
        protected override void OnTick()
        {
            // Read signals every 5 seconds
            if ((Server.Time - _lastSignalRead).TotalSeconds >= 5)
            {
                ReadSignals();
                _lastSignalRead = Server.Time;
            }
        }
        
        protected override void OnBar()
        {
            // Write market data on every bar close
            WriteMarketData();
            
            // Execute Claude decision
            ExecuteDecision();
        }
        
        private void ReadSignals()
        {
            try
            {
                if (!File.Exists(_signalsFile)) return;
                
                string json = File.ReadAllText(_signalsFile, Encoding.UTF8);
                _lastSignal = JsonSerializer.Deserialize<SignalsData>(json);
            }
            catch (Exception ex)
            {
                Print("Read error: " + ex.Message);
            }
        }
        
        private void WriteMarketData()
        {
            try
            {
                var data = new
                {
                    symbol = SymbolName,
                    timestamp = Server.Time.ToString("yyyy-MM-ddTHH:mm:ssZ"),
                    current_price = Symbol.Bid,
                    spread = Symbol.Spread / Symbol.PipSize,
                    positions = GetPositionsJson(),
                };
                
                string json = JsonSerializer.Serialize(data);
                string tmp = _marketDataFile + ".tmp";
                File.WriteAllText(tmp, json, Encoding.UTF8);
                
                if (File.Exists(_marketDataFile))
                    File.Delete(_marketDataFile);
                File.Move(tmp, _marketDataFile);
            }
            catch (Exception ex)
            {
                Print("Write error: " + ex.Message);
            }
        }
        
        private void ExecuteDecision()
        {
            if (_lastSignal == null || string.IsNullOrEmpty(_lastSignal.Action))
                return;
            
            string action = _lastSignal.Action.ToUpper();
            
            switch (action)
            {
                case "BUY":
                    ExecuteBuy();
                    break;
                case "SELL":
                    ExecuteSell();
                    break;
                case "CLOSE":
                    CloseAllPositions();
                    break;
                case "WAIT":
                    Print("WAIT signal received");
                    break;
            }
        }
        
        private void ExecuteBuy()
        {
            // Check if already have a position
            foreach (var pos in Positions)
            {
                if (pos.SymbolName == SymbolName && pos.TradeType == TradeType.Buy)
                {
                    Print("BUY position already open");
                    return;
                }
            }
            
            double sl = _lastSignal.SlPrice;
            double tp = _lastSignal.TpPrice;
            
            // Validate SL distance (full validation logic proprietary)
            double slPoints = Math.Abs(Symbol.Ask - sl);
            if (slPoints < SlMinPoints || slPoints > SlMaxPoints)
            {
                Print("SL out of range: {0} points", slPoints);
                return;
            }
            
            // Calculate volume (formula proprietary - placeholder)
            double volume = CalculateVolume(slPoints);
            
            // Execute trade
            var result = ExecuteMarketOrder(TradeType.Buy, SymbolName, volume, "ClaudeBot");
            
            if (result.IsSuccessful)
            {
                ModifyPosition(result.Position, sl, tp);
                Print("BUY executed: SL={0} TP={1}", sl, tp);
            }
            else
            {
                Print("BUY failed: " + result.Error);
            }
        }
        
        private void ExecuteSell()
        {
            // Similar to Buy
            foreach (var pos in Positions)
            {
                if (pos.SymbolName == SymbolName && pos.TradeType == TradeType.Sell)
                {
                    Print("SELL position already open");
                    return;
                }
            }
            
            double sl = _lastSignal.SlPrice;
            double tp = _lastSignal.TpPrice;
            
            double slPoints = Math.Abs(Symbol.Bid - sl);
            if (slPoints < SlMinPoints || slPoints > SlMaxPoints)
            {
                Print("SL out of range: {0} points", slPoints);
                return;
            }
            
            double volume = CalculateVolume(slPoints);
            var result = ExecuteMarketOrder(TradeType.Sell, SymbolName, volume, "ClaudeBot");
            
            if (result.IsSuccessful)
            {
                ModifyPosition(result.Position, sl, tp);
                Print("SELL executed: SL={0} TP={1}", sl, tp);
            }
        }
        
        private double CalculateVolume(double slPoints)
        {
            /**
             * VOLUME CALCULATION (proprietary)
             * 
             * Formula: volume = risk_amount / (sl_points * value_per_point)
             * where value_per_point depends on broker's PipSize/PipValue
             * 
             * Full implementation not included in demo.
             */
            double riskAmount = Account.Balance * (RiskPerTradePct / 100.0);
            
            // Placeholder - actual formula proprietary
            double valuePerPoint = 1.0;
            double volume = riskAmount / (slPoints * valuePerPoint);
            
            return Symbol.NormalizeVolumeInUnits(volume, RoundingMode.Down);
        }
        
        private void CloseAllPositions()
        {
            foreach (var pos in Positions)
            {
                if (pos.SymbolName == SymbolName)
                {
                    ClosePosition(pos);
                    Print("Position closed");
                }
            }
        }
        
        private string GetPositionsJson()
        {
            // Format positions as JSON string
            return "[]";  // Simplified
        }
    }
    
    public class SignalsData
    {
        public string Action { get; set; }
        public double SlPrice { get; set; }
        public double TpPrice { get; set; }
        public int Confidence { get; set; }
        public string Reasoning { get; set; }
    }
}