import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import requests
import json
import threading
import time
import datetime
import pandas as pd
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import yfinance as yf
from collections import deque
import os
import pickle

class CryptoTradingBot:
    def __init__(self, root):
        self.root = root
        self.root.title("Crypto Trading Bot - Futhi Jr Simelane")
        self.root.geometry("1400x900")
        self.root.configure(bg='#0a0a0a')
        
        # Trading state
        self.is_trading = False
        self.paper_trading = True
        self.current_strategy = "Moving Average"
        
        # Data storage
        self.price_history = deque(maxlen=1000)
        self.portfolio = {
            'cash': 10000.0,
            'crypto': 0.0,
            'total_value': 10000.0,
            'trades': []
        }
        
        # Trading parameters
        self.symbol = "BTC-USD"
        self.update_interval = 5  # seconds
        self.strategy_params = {
            'Moving Average': {'short_window': 10, 'long_window': 30},
            'RSI': {'period': 14, 'oversold': 30, 'overbought': 70},
            'MACD': {'fast': 12, 'slow': 26, 'signal': 9}
        }
        
        # API endpoints
        self.api_url = "https://query1.finance.yahoo.com/v8/finance/chart/"
        
        self.setup_gui()
        self.load_portfolio()
        
    def setup_gui(self):
        # Main container
        main_frame = tk.Frame(self.root, bg='#0a0a0a')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_frame = tk.Frame(main_frame, bg='#0a0a0a')
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = tk.Label(title_frame, text="🚀 Crypto Trading Bot", 
                              font=('Arial', 24, 'bold'), 
                              fg='#00ff88', bg='#0a0a0a')
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame, text="Real-time Trading with AI Strategies", 
                                 font=('Arial', 12), 
                                 fg='#888888', bg='#0a0a0a')
        subtitle_label.pack()
        
        # Control panel
        control_frame = tk.Frame(main_frame, bg='#1a1a1a', relief=tk.RAISED, bd=2)
        control_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Left side controls
        left_controls = tk.Frame(control_frame, bg='#1a1a1a')
        left_controls.pack(side=tk.LEFT, padx=20, pady=20)
        
        # Symbol selection
        tk.Label(left_controls, text="Trading Pair:", font=('Arial', 10, 'bold'), 
                fg='#ffffff', bg='#1a1a1a').pack(anchor=tk.W)
        
        self.symbol_var = tk.StringVar(value="BTC-USD")
        symbol_combo = ttk.Combobox(left_controls, textvariable=self.symbol_var, 
                                   values=["BTC-USD", "ETH-USD", "ADA-USD", "DOT-USD", "LINK-USD"],
                                   state="readonly", width=15)
        symbol_combo.pack(pady=(5, 15))
        symbol_combo.bind('<<ComboboxSelected>>', self.on_symbol_change)
        
        # Strategy selection
        tk.Label(left_controls, text="Trading Strategy:", font=('Arial', 10, 'bold'), 
                fg='#ffffff', bg='#1a1a1a').pack(anchor=tk.W)
        
        self.strategy_var = tk.StringVar(value="Moving Average")
        strategy_combo = ttk.Combobox(left_controls, textvariable=self.strategy_var, 
                                     values=["Moving Average", "RSI", "MACD"],
                                     state="readonly", width=15)
        strategy_combo.pack(pady=(5, 15))
        strategy_combo.bind('<<ComboboxSelected>>', self.on_strategy_change)
        
        # Trading mode
        self.paper_trading_var = tk.BooleanVar(value=True)
        paper_check = tk.Checkbutton(left_controls, text="Paper Trading Mode", 
                                    variable=self.paper_trading_var, 
                                    fg='#ffffff', bg='#1a1a1a', selectcolor='#333333',
                                    font=('Arial', 10))
        paper_check.pack(anchor=tk.W, pady=(0, 15))
        
        # Start/Stop button
        self.trading_button = tk.Button(left_controls, text="🚀 Start Trading", 
                                       command=self.toggle_trading,
                                       bg='#00ff88', fg='#000000', 
                                       font=('Arial', 12, 'bold'),
                                       relief=tk.FLAT, padx=20, pady=10)
        self.trading_button.pack(pady=(0, 15))
        
        # Right side - Portfolio display
        right_controls = tk.Frame(control_frame, bg='#1a1a1a')
        right_controls.pack(side=tk.RIGHT, padx=20, pady=20)
        
        # Portfolio info
        tk.Label(right_controls, text="Portfolio Status", font=('Arial', 12, 'bold'), 
                fg='#00ff88', bg='#1a1a1a').pack(anchor=tk.W)
        
        self.cash_label = tk.Label(right_controls, text="Cash: $10,000.00", 
                                  font=('Arial', 10), fg='#ffffff', bg='#1a1a1a')
        self.cash_label.pack(anchor=tk.W, pady=2)
        
        self.crypto_label = tk.Label(right_controls, text="Crypto: 0.0000", 
                                    font=('Arial', 10), fg='#ffffff', bg='#1a1a1a')
        self.crypto_label.pack(anchor=tk.W, pady=2)
        
        self.total_label = tk.Label(right_controls, text="Total Value: $10,000.00", 
                                   font=('Arial', 10, 'bold'), fg='#00ff88', bg='#1a1a1a')
        self.total_label.pack(anchor=tk.W, pady=2)
        
        # Current price display
        self.price_label = tk.Label(right_controls, text="Current Price: $0.00", 
                                   font=('Arial', 12, 'bold'), fg='#ffaa00', bg='#1a1a1a')
        self.price_label.pack(anchor=tk.W, pady=(15, 5))
        
        # Main content area
        content_frame = tk.Frame(main_frame, bg='#0a0a0a')
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Chart area
        chart_frame = tk.Frame(content_frame, bg='#1a1a1a', relief=tk.RAISED, bd=2)
        chart_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        tk.Label(chart_frame, text="Price Chart & Indicators", font=('Arial', 12, 'bold'), 
                fg='#ffffff', bg='#1a1a1a').pack(pady=10)
        
        # Create matplotlib figure
        self.fig = Figure(figsize=(10, 6), facecolor='#1a1a1a')
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor('#1a1a1a')
        self.ax.tick_params(colors='#ffffff')
        self.ax.spines['bottom'].set_color('#ffffff')
        self.ax.spines['top'].set_color('#ffffff')
        self.ax.spines['left'].set_color('#ffffff')
        self.ax.spines['right'].set_color('#ffffff')
        
        self.canvas = FigureCanvasTkAgg(self.fig, chart_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Trading log area
        log_frame = tk.Frame(content_frame, bg='#1a1a1a', relief=tk.RAISED, bd=2)
        log_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0))
        
        tk.Label(log_frame, text="Trading Log", font=('Arial', 12, 'bold'), 
                fg='#ffffff', bg='#1a1a1a').pack(pady=10)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, width=40, height=20, 
                                                 bg='#0a0a0a', fg='#00ff88',
                                                 font=('Consolas', 9))
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Initialize chart
        self.update_chart()
        
    def on_symbol_change(self, event=None):
        self.symbol = self.symbol_var.get()
        self.price_history.clear()
        self.log_message(f"Switched to {self.symbol}")
        
    def on_strategy_change(self, event=None):
        self.current_strategy = self.strategy_var.get()
        self.log_message(f"Strategy changed to {self.current_strategy}")
        
    def toggle_trading(self):
        if not self.is_trading:
            self.is_trading = True
            self.trading_button.config(text="⏹️ Stop Trading", bg='#ff4757')
            self.log_message("🚀 Trading started!")
            self.start_trading_thread()
        else:
            self.is_trading = False
            self.trading_button.config(text="🚀 Start Trading", bg='#00ff88')
            self.log_message("⏹️ Trading stopped!")
            
    def start_trading_thread(self):
        trading_thread = threading.Thread(target=self.trading_loop, daemon=True)
        trading_thread.start()
        
    def trading_loop(self):
        while self.is_trading:
            try:
                # Get current price
                current_price = self.get_current_price()
                if current_price:
                    self.price_history.append({
                        'timestamp': datetime.datetime.now(),
                        'price': current_price
                    })
                    
                    # Update GUI
                    self.root.after(0, self.update_price_display, current_price)
                    self.root.after(0, self.update_chart)
                    
                    # Check for trading signals
                    signal = self.get_trading_signal()
                    if signal:
                        self.execute_trade(signal, current_price)
                        
                time.sleep(self.update_interval)
                
            except Exception as e:
                self.log_message(f"Error in trading loop: {str(e)}")
                time.sleep(self.update_interval)
                
    def get_current_price(self):
        try:
            ticker = yf.Ticker(self.symbol)
            current_price = ticker.info['regularMarketPrice']
            return current_price
        except:
            return None
            
    def update_price_display(self, price):
        self.price_label.config(text=f"Current Price: ${price:,.2f}")
        
    def get_trading_signal(self):
        if len(self.price_history) < 50:
            return None
            
        prices = [p['price'] for p in self.price_history]
        
        if self.current_strategy == "Moving Average":
            return self.moving_average_strategy(prices)
        elif self.current_strategy == "RSI":
            return self.rsi_strategy(prices)
        elif self.current_strategy == "MACD":
            return self.macd_strategy(prices)
            
    def moving_average_strategy(self, prices):
        short_window = self.strategy_params['Moving Average']['short_window']
        long_window = self.strategy_params['Moving Average']['long_window']
        
        if len(prices) < long_window:
            return None
            
        short_ma = np.mean(prices[-short_window:])
        long_ma = np.mean(prices[-long_window:])
        
        # Buy signal: short MA crosses above long MA
        if short_ma > long_ma and len(prices) >= 2:
            prev_short_ma = np.mean(prices[-short_window-1:-1])
            prev_long_ma = np.mean(prices[-long_window-1:-1])
            if prev_short_ma <= prev_long_ma:
                return "BUY"
                
        # Sell signal: short MA crosses below long MA
        elif short_ma < long_ma and len(prices) >= 2:
            prev_short_ma = np.mean(prices[-short_window-1:-1])
            prev_long_ma = np.mean(prices[-long_window-1:-1])
            if prev_short_ma >= prev_long_ma:
                return "SELL"
                
        return None
        
    def rsi_strategy(self, prices):
        period = self.strategy_params['RSI']['period']
        oversold = self.strategy_params['RSI']['oversold']
        overbought = self.strategy_params['RSI']['overbought']
        
        if len(prices) < period + 1:
            return None
            
        # Calculate RSI
        deltas = np.diff(prices)
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)
        
        avg_gain = np.mean(gains[-period:])
        avg_loss = np.mean(losses[-period:])
        
        if avg_loss == 0:
            rsi = 100
        else:
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
            
        # Trading signals
        if rsi < oversold:
            return "BUY"
        elif rsi > overbought:
            return "SELL"
            
        return None
        
    def macd_strategy(self, prices):
        fast = self.strategy_params['MACD']['fast']
        slow = self.strategy_params['MACD']['slow']
        signal = self.strategy_params['MACD']['signal']
        
        if len(prices) < slow + signal:
            return None
            
        # Calculate MACD
        ema_fast = self.calculate_ema(prices, fast)
        ema_slow = self.calculate_ema(prices, slow)
        macd_line = ema_fast - ema_slow
        
        # Calculate signal line
        macd_values = []
        for i in range(len(prices) - slow + 1):
            ema_f = self.calculate_ema(prices[i:i+slow], fast)
            ema_s = self.calculate_ema(prices[i:i+slow], slow)
            macd_values.append(ema_f - ema_s)
            
        signal_line = self.calculate_ema(macd_values, signal)
        
        # Trading signals
        if macd_line > signal_line and len(macd_values) >= 2:
            prev_macd = macd_values[-2]
            prev_signal = self.calculate_ema(macd_values[:-1], signal)
            if prev_macd <= prev_signal:
                return "BUY"
        elif macd_line < signal_line and len(macd_values) >= 2:
            prev_macd = macd_values[-2]
            prev_signal = self.calculate_ema(macd_values[:-1], signal)
            if prev_macd >= prev_signal:
                return "SELL"
                
        return None
        
    def calculate_ema(self, prices, period):
        if len(prices) < period:
            return np.mean(prices)
            
        alpha = 2 / (period + 1)
        ema = prices[0]
        
        for price in prices[1:]:
            ema = alpha * price + (1 - alpha) * ema
            
        return ema
        
    def execute_trade(self, signal, price):
        if signal == "BUY" and self.portfolio['cash'] > 0:
            # Buy with 95% of available cash
            buy_amount = self.portfolio['cash'] * 0.95
            crypto_amount = buy_amount / price
            
            self.portfolio['cash'] -= buy_amount
            self.portfolio['crypto'] += crypto_amount
            
            trade = {
                'timestamp': datetime.datetime.now(),
                'action': 'BUY',
                'price': price,
                'amount': crypto_amount,
                'value': buy_amount
            }
            self.portfolio['trades'].append(trade)
            
            self.log_message(f"🟢 BUY: {crypto_amount:.4f} {self.symbol.split('-')[0]} at ${price:,.2f}")
            
        elif signal == "SELL" and self.portfolio['crypto'] > 0:
            # Sell 95% of crypto holdings
            sell_amount = self.portfolio['crypto'] * 0.95
            cash_value = sell_amount * price
            
            self.portfolio['crypto'] -= sell_amount
            self.portfolio['cash'] += cash_value
            
            trade = {
                'timestamp': datetime.datetime.now(),
                'action': 'SELL',
                'price': price,
                'amount': sell_amount,
                'value': cash_value
            }
            self.portfolio['trades'].append(trade)
            
            self.log_message(f"🔴 SELL: {sell_amount:.4f} {self.symbol.split('-')[0]} at ${price:,.2f}")
            
        # Update portfolio display
        self.update_portfolio_display()
        self.save_portfolio()
        
    def update_portfolio_display(self):
        current_price = self.get_current_price()
        if current_price:
            crypto_value = self.portfolio['crypto'] * current_price
            total_value = self.portfolio['cash'] + crypto_value
            self.portfolio['total_value'] = total_value
            
            self.cash_label.config(text=f"Cash: ${self.portfolio['cash']:,.2f}")
            self.crypto_label.config(text=f"Crypto: {self.portfolio['crypto']:.4f}")
            self.total_label.config(text=f"Total Value: ${total_value:,.2f}")
            
    def update_chart(self):
        if len(self.price_history) < 2:
            return
            
        self.ax.clear()
        self.ax.set_facecolor('#1a1a1a')
        self.ax.tick_params(colors='#ffffff')
        
        timestamps = [p['timestamp'] for p in self.price_history]
        prices = [p['price'] for p in self.price_history]
        
        # Plot price line
        self.ax.plot(timestamps, prices, color='#00ff88', linewidth=2, label='Price')
        
        # Add moving averages if enough data
        if len(prices) >= 30:
            short_ma = [np.mean(prices[max(0, i-10):i+1]) for i in range(len(prices))]
            long_ma = [np.mean(prices[max(0, i-30):i+1]) for i in range(len(prices))]
            
            self.ax.plot(timestamps, short_ma, color='#ffaa00', linewidth=1, label='Short MA')
            self.ax.plot(timestamps, long_ma, color='#ff4757', linewidth=1, label='Long MA')
            
        self.ax.set_title(f'{self.symbol} Price Chart', color='#ffffff', fontsize=14)
        self.ax.set_xlabel('Time', color='#ffffff')
        self.ax.set_ylabel('Price ($)', color='#ffffff')
        self.ax.legend()
        self.ax.grid(True, alpha=0.3, color='#333333')
        
        # Rotate x-axis labels
        plt.setp(self.ax.get_xticklabels(), rotation=45)
        
        self.canvas.draw()
        
    def log_message(self, message):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        
    def save_portfolio(self):
        try:
            with open('portfolio_data.pkl', 'wb') as f:
                pickle.dump(self.portfolio, f)
        except Exception as e:
            print(f"Error saving portfolio: {e}")
            
    def load_portfolio(self):
        try:
            if os.path.exists('portfolio_data.pkl'):
                with open('portfolio_data.pkl', 'rb') as f:
                    self.portfolio = pickle.load(f)
                    self.update_portfolio_display()
        except Exception as e:
            print(f"Error loading portfolio: {e}")

def main():
    root = tk.Tk()
    app = CryptoTradingBot(root)
    root.mainloop()

if __name__ == "__main__":
    main() 