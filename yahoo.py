import yfinance as yf
import pandas as pd
import numpy as np

# Download historical data for stocks
data = yf.download('LSXMA', start='2023-06-01', end='2024-03-10')

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


def plot_full_chart_with_signals(data):
    plt.figure(figsize=(14, 12))

    # First subplot for Adjusted Close Price with Buy/Sell Signals
    plt.subplot(3, 1, 1)  # 3 rows, 1 column, 1st subplot
    plt.plot(data.index, data['Adj Close'], label='Adj Close')
    plt.title('Adjusted Close Price with Buy/Sell Signals')

    # Highlight buy signals on the adjusted close price chart
    buy_signals = data[data['Buy Signal'] == True]
    plt.scatter(buy_signals.index, buy_signals['Adj Close'], label='Buy Signal', color='green', marker='^', s=100)

    # Highlight sell signals on the adjusted close price chart
    sell_signals = data[data['Sell Signal'] == True]
    plt.scatter(sell_signals.index, sell_signals['Adj Close'], label='Sell Signal', color='red', marker='v', s=100)

    plt.legend()

    # Second subplot for Impulse MACD ('md'), Signal ('sb'), and Histogram ('sh')
    plt.subplot(3, 1, 2)  # 3 rows, 1 column, 2nd subplot
    plt.bar(data.index, data['sh'], label='Impulse Histogram (sh)', color='grey', alpha=0.3)
    plt.plot(data.index, data['md'], label='Impulse MACD (md)', color='blue')
    plt.plot(data.index, data['sb'], label='Signal (sb)', color='red', linestyle='--')
    plt.title('Impulse MACD')

    # Highlight buy signals
    plt.scatter(buy_signals.index, buy_signals['md'], label='Buy Signal (MACD)', color='green', marker='^', s=100)

    # Highlight sell signals
    plt.scatter(sell_signals.index, sell_signals['md'], label='Sell Signal (MACD)', color='red', marker='v', s=100)

    plt.legend()

    # Third subplot for Relative Strength Index (RSI)
    plt.subplot(3, 1, 3)  # 3 rows, 1 column, 3rd subplot
    plt.plot(data.index, data['RSI'], label='RSI', color='purple')
    plt.title('Relative Strength Index (RSI)')
    plt.axhline(70, linestyle='--', color='red', alpha=0.5)  # Overbought line
    plt.axhline(30, linestyle='--', color='green', alpha=0.5)  # Oversold line
    plt.legend()

    # Format the x-axis for all subplots
    for i in range(1, 4):
        plt.subplot(3, 1, i)
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
        plt.gcf().autofmt_xdate()  # Rotation

    plt.tight_layout()  # Adjust subplots to fit into the figure area.
    plt.show()

# Call the function with your data frame to visualize the charts
plot_full_chart_with_signals(data_omit)



###################################### BACKTEST

import pandas as pd

# Your initial capital and other settings
initial_capital = 100000
capital = initial_capital
position = 0  # To track how many shares are held
in_position = False

# Lists to store the value of the portfolio over time
portfolio_values = []

for date, row in data_omit.iterrows():
    # Check for buy signal and if we're not already in position
    if row['Buy Signal'] and not in_position:
        # Calculate how many shares we can buy
        shares_to_buy = capital // row['Adj Close']
        cost_of_buy = shares_to_buy * row['Adj Close']
        capital -= cost_of_buy
        position += shares_to_buy
        in_position = True
        print(f"Buying {shares_to_buy} shares on {date} at {row['Adj Close']}")

    # Check for sell signal and if we are in position
    elif row['Sell Signal'] and in_position:
        # Calculate the value of selling the shares
        value_of_sell = position * row['Adj Close']
        capital += value_of_sell
        print(f"Selling {position} shares on {date} at {row['Adj Close']}")
        position = 0
        in_position = False

    # Update the portfolio value for each day
    portfolio_value = capital + (position * row['Adj Close'])
    portfolio_values.append(portfolio_value)

# Convert the portfolio values list into a pandas Series for easy plotting and analysis
portfolio_values_series = pd.Series(portfolio_values, index=data_omit.index)

# Print the final portfolio value
final_portfolio_value = portfolio_values_series.iloc[-1]
print(f"Final portfolio value: ${final_portfolio_value:,.2f} after starting with ${initial_capital:,.2f}")
print(f"Profit / Loss: ${final_portfolio_value - initial_capital:,.2f}")

# Plotting the portfolio value over time
import matplotlib.pyplot as plt

plt.figure(figsize=(14, 7))
portfolio_values_series.plot(title='Portfolio Value Over Time')
plt.xlabel('Date')
plt.ylabel('Portfolio Value ($)')
plt.show()



# Example: Downloading historical data for the SPY ETF as a benchmark
benchmark_data = yf.download('AAPL', start='2023-06-01', end='2024-03-10')['Adj Close']

initial_capital = 100000  # Assuming the same initial capital as your strategy

# Calculate daily returns of the benchmark
benchmark_returns = benchmark_data.pct_change()

# Calculate cumulative returns by adding 1 and then calculating the cumulative product
benchmark_cumulative_returns = (1 + benchmark_returns).cumprod()

# Calculate the benchmark portfolio value series
benchmark_values_series = initial_capital * benchmark_cumulative_returns


# Calculate performance metrics for both
from scipy.stats import ttest_ind

# Example: Comparing annualized returns
annualized_return_strategy = portfolio_values_series.pct_change().mean() * 252
annualized_return_benchmark = benchmark_values_series.pct_change().mean() * 252

print(f"Strategy Annualized Return: {annualized_return_strategy}")
print(f"Benchmark Annualized Return: {annualized_return_benchmark}")

# Statistical Test Example: Comparing daily returns
t_stat, p_value = ttest_ind(portfolio_values_series.pct_change().dropna(), benchmark_values_series.pct_change().dropna())

print(f"T-statistic: {t_stat}, P-value: {p_value}")
# A small p-value (< 0.05) might indicate a statistically significant difference in daily returns

# Visual Comparison
plt.figure(figsize=(14, 7))
plt.plot(portfolio_values_series, label='Strategy')
plt.plot(benchmark_values_series, label='Benchmark')
plt.title('Portfolio Value: Strategy vs. Benchmark')
plt.xlabel('Date')
plt.ylabel('Portfolio Value')
plt.legend()
plt.show()