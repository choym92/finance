import yfinance as yf
import pandas as pd
import numpy as np

# Download historical data for stocks
data = yf.download('SPY', start='2023-06-01', end='2024-03-10')

# Calculate price changes
data['Delta'] = data['Adj Close'].diff()

# Separate gains and losses
data['Gain'] = data['Delta'].clip(lower=0)
data['Loss'] = -data['Delta'].clip(upper=0)

# Calculate the Exponential Moving Average (EMA) of gains and losses
alpha = 1/14  # For a 14-day RSI
data['Avg Gain'] = data['Gain'].ewm(alpha=alpha, adjust=False).mean()
data['Avg Loss'] = data['Loss'].ewm(alpha=alpha, adjust=False).mean()

# Calculate the Relative Strength (RS)
data['RS'] = data['Avg Gain'] / data['Avg Loss']

# Calculate the RSI
data['RSI'] = 100 - (100 / (1 + data['RS']))

# Calculate MACD

# Calculate SMMA (Smoothed Moving Average) for High and Low as proxies for hi and lo in LazyBear's code
lengthMA = 34  # Example length
data['hi'] = data['High'].ewm(span=lengthMA, adjust=False).mean()
data['lo'] = data['Low'].ewm(span=lengthMA, adjust=False).mean()

# mi as ZLEMA of the hlc3, using an EMA of EMA as a proxy
data['hlc3'] = (data['High'] + data['Low'] + data['Close']) / 3
data['ema1'] = data['hlc3'].ewm(span=lengthMA, adjust=False).mean()
data['ema2'] = data['ema1'].ewm(span=lengthMA, adjust=False).mean()
data['mi'] = data['ema1'] + (data['ema1'] - data['ema2'])

# md calculation (proxy for md), noting we don't have the exact method but approximate as difference from mi to hi/lo
data['md'] = data.apply(lambda row: (row['mi'] - row['hi']) if row['mi'] > row['hi'] else (row['mi'] - row['lo']) if row['mi'] < row['lo'] else 0, axis=1)

# sb and sh calculations
lengthSignal = 9
data['sb'] = data['md'].rolling(window=lengthSignal).mean()
data['sh'] = data['md'] - data['sb']

# Using md, sb, and sh to define buy signals based on LazyBear's idea
# Without specific conditions from LazyBear's code, we define a buy signal when md moves above sb as an indication of bullish impulse
data['Buy Signal'] = (data['md'] > data['sb']) & (data['md'].shift(1) <= data['sb'].shift(1))
data['Sell Signal'] = (data['md'] < data['sb']) & (data['md'].shift(1) >= data['sb'].shift(1))

# Select relevant columns for the buy signal
buy_signals = data[data['Buy Signal']]

print(buy_signals[['Adj Close', 'hi', 'lo', 'mi', 'md', 'sb', 'sh', 'Buy Signal', 'RSI']])

data_omit = data[40:]

##########################################

import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def plot_chart(data): 
    
    # Assuming 'data' is your DataFrame with the necessary columns including RSI
    
    # Create a new figure and set the size
    plt.figure(figsize=(14, 10))
    
    # Plot the adjusted close price
    plt.subplot(3, 1, 1)  # 3 rows, 1 column, 1st subplot
    plt.plot(data.index, data['Adj Close'], label='Adj Close')
    plt.title('Adjusted Close Price')
    plt.legend()
    
    # Plot Impulse MACD ('md'), Signal ('sb'), and Histogram ('sh')
    plt.subplot(3, 1, 2)  # 3 rows, 1 column, 2nd subplot
    plt.bar(data.index, data['sh'], label='Impulse Histogram (sh)', color='grey', alpha=0.3)
    plt.plot(data.index, data['md'], label='Impulse MACD (md)', color='blue')
    plt.plot(data.index, data['sb'], label='Signal (sb)', color='red', linestyle='--')
    plt.title('Impulse MACD')
    
    # Highlight buy signals
    buy_signals = data[data['Buy Signal'] == True]
    plt.scatter(buy_signals.index, buy_signals['md'], label='Buy Signal', color='green', marker='^', alpha=1)
    
    # Highlight sell signals
    sell_signals = data[data['Sell Signal'] == True]
    plt.scatter(sell_signals.index, sell_signals['md'], label='Sell Signal', color='red', marker='v', alpha=1)
    
    plt.legend()
    
    # Plot RSI
    plt.subplot(3, 1, 3)  # 3 rows, 1 column, 3rd subplot
    plt.plot(data.index, data['RSI'], label='RSI', color='purple')
    plt.title('Relative Strength Index (RSI)')
    plt.axhline(70, linestyle='--', color='red', alpha=0.5)  # Overbought line
    plt.axhline(30, linestyle='--', color='green', alpha=0.5)  # Oversold line
    plt.legend()
    
    # Format the x-axis
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.gcf().autofmt_xdate()  # Rotation
    
    plt.tight_layout()  # Adjust subplots to fit into the figure area.
    plt.show()


# omit first 40 days so i can have a correct view of the stock

plot_chart(data_omit)












#######################################






# MACD Line: 12-day EMA - 26-day EMA
data['EMA12'] = data['Adj Close'].ewm(span=12, adjust=False).mean()
data['EMA26'] = data['Adj Close'].ewm(span=26, adjust=False).mean()
data['MACD'] = data['EMA12'] - data['EMA26']

# Signal Line: 9-day EMA of MACD Line
data['Signal Line'] = data['MACD'].ewm(span=9, adjust=False).mean()

# MACD Histogram: MACD Line - Signal Line
data['MACD Histogram'] = data['MACD'] - data['Signal Line']

# Select relevant columns to display
print(data[['Adj Close', 'RSI', 'MACD', 'Signal Line', 'MACD Histogram']])