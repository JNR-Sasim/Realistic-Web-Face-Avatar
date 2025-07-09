# 🚀 Crypto Trading Bot

A sophisticated automated cryptocurrency trading bot built with Python, featuring real-time data analysis, multiple trading strategies, and a beautiful GUI interface.

## ✨ Features

### 🎯 Trading Strategies
- **Moving Average Crossover**: Uses short and long-term moving averages to identify trend changes
- **RSI (Relative Strength Index)**: Identifies overbought and oversold conditions
- **MACD (Moving Average Convergence Divergence)**: Advanced momentum indicator

### 📊 Real-time Features
- Live price tracking from Yahoo Finance API
- Real-time portfolio value calculation
- Interactive price charts with technical indicators
- Live trading log with timestamps

### 🛡️ Safety Features
- **Paper Trading Mode**: Test strategies without real money
- Risk management with position sizing
- Portfolio tracking and trade history
- Automatic data persistence

### 🎨 User Interface
- Modern dark theme with neon accents
- Real-time price updates
- Interactive charts using Matplotlib
- Comprehensive trading log
- Portfolio status dashboard

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Internet connection for real-time data

### Installation

1. **Clone or download the project**
2. **Install dependencies:**
   ```bash
   pip install -r trading_bot_requirements.txt
   ```

3. **Run the bot:**
   ```bash
   python crypto_trading_bot.py
   ```

## 📖 How to Use

### 1. Initial Setup
- Select your preferred cryptocurrency pair (BTC-USD, ETH-USD, etc.)
- Choose a trading strategy
- Enable "Paper Trading Mode" for safe testing

### 2. Start Trading
- Click "🚀 Start Trading" to begin
- The bot will automatically:
  - Fetch real-time price data
  - Apply your selected strategy
  - Execute trades based on signals
  - Update your portfolio

### 3. Monitor Performance
- Watch the live price chart
- Check the trading log for executed trades
- Monitor your portfolio value in real-time

## 📈 Trading Strategies Explained

### Moving Average Crossover
- **Buy Signal**: Short-term MA crosses above long-term MA
- **Sell Signal**: Short-term MA crosses below long-term MA
- **Best for**: Trend-following markets

### RSI Strategy
- **Buy Signal**: RSI drops below 30 (oversold)
- **Sell Signal**: RSI rises above 70 (overbought)
- **Best for**: Range-bound markets

### MACD Strategy
- **Buy Signal**: MACD line crosses above signal line
- **Sell Signal**: MACD line crosses below signal line
- **Best for**: Momentum trading

## ⚙️ Configuration

### Strategy Parameters
You can modify strategy parameters in the code:

```python
self.strategy_params = {
    'Moving Average': {'short_window': 10, 'long_window': 30},
    'RSI': {'period': 14, 'oversold': 30, 'overbought': 70},
    'MACD': {'fast': 12, 'slow': 26, 'signal': 9}
}
```

### Trading Parameters
- **Update Interval**: How often to check for new data (default: 5 seconds)
- **Position Size**: Percentage of portfolio to trade (default: 95%)
- **Initial Capital**: Starting portfolio value (default: $10,000)

## 🔧 Customization

### Adding New Strategies
1. Create a new strategy function
2. Add it to the `get_trading_signal()` method
3. Update the strategy selection dropdown

### Adding New Cryptocurrencies
1. Add the symbol to the symbol combo box
2. Ensure it's available on Yahoo Finance

### Modifying Risk Management
- Adjust position sizing in `execute_trade()`
- Add stop-loss mechanisms
- Implement portfolio rebalancing

## 📊 Portfolio Management

The bot automatically tracks:
- Available cash
- Cryptocurrency holdings
- Total portfolio value
- Trade history with timestamps
- Performance metrics

## 🛡️ Safety Warnings

⚠️ **Important Disclaimers:**
- This is for educational purposes
- Always use paper trading mode first
- Cryptocurrency trading involves significant risk
- Past performance doesn't guarantee future results
- Never invest more than you can afford to lose

## 🐛 Troubleshooting

### Common Issues

**"No module named 'yfinance'"**
```bash
pip install yfinance
```

**Chart not updating**
- Check internet connection
- Verify the cryptocurrency symbol is valid

**Trading not executing**
- Ensure you have sufficient funds
- Check if paper trading mode is enabled

## 📁 File Structure

```
crypto_trading_bot.py          # Main application
trading_bot_requirements.txt   # Python dependencies
TRADING_BOT_README.md         # This file
portfolio_data.pkl            # Saved portfolio data (auto-generated)
```

## 🔮 Future Enhancements

- [ ] Multiple cryptocurrency support
- [ ] Advanced risk management
- [ ] Backtesting capabilities
- [ ] Machine learning strategies
- [ ] Web-based interface
- [ ] Mobile notifications
- [ ] Integration with real exchanges

## 👨‍💻 Developer

**Created by:** Futhi Jr Simelane

This project demonstrates advanced Python programming concepts including:
- Real-time data processing
- GUI development with Tkinter
- Financial analysis and algorithms
- Multi-threading for concurrent operations
- Data visualization with Matplotlib
- API integration and error handling

## 📄 License

This project is for educational purposes. Use at your own risk.

---

**Happy Trading! 🚀📈** 