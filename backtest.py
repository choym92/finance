import alpaca_trade_api as tradeapi
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from api_keys import *  # Make sure this file exists and is correctly configured

# Alpaca API credentials
API_KEY = ALPACA_TRADER_API_KEY
API_SECRET = ALPACA_TRADER_API_SECRET
BASE_URL = 'https://paper-api.alpaca.markets'  # Use paper trading base URL for testing

# Initialize Alpaca API
api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')


def backtest(symbol, start_date, end_date, short_window, long_window, initial_cash, rsi_period=14, rsi_overbought=70, rsi_oversold=30):
    # Retrieve historical price data
    barset = api.get_bars(symbol, '1D', start=start_date, end=end_date).df
    df = pd.DataFrame(barset)

    # Calculate short and long moving averages
    df['Short_MAVG'] = df['close'].rolling(window=short_window).mean()
    df['Long_MAVG'] = df['close'].rolling(window=long_window).mean()

    # Generate moving average crossover signals
    df['MA_Signal'] = 0
    df.loc[df['Short_MAVG'] > df['Long_MAVG'], 'MA_Signal'] = 1  # Bullish trend
    df.loc[df['Short_MAVG'] < df['Long_MAVG'], 'MA_Signal'] = -1  # Bearish trend

    # Calculate RSI
    delta = df['close'].diff(1)
    gain = (delta.where(delta > 0, 0)).rolling(window=rsi_period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=rsi_period).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))

    # Initialize portfolio variables
    cash = initial_cash
    shares_owned = 0
    portfolio_values = []
    shares_owned_list = []

    # Iterate through DataFrame for buy/sell signals
    for i, row in df.iterrows():
        # Check for buying opportunity within bullish trend
        if row['MA_Signal'] == 1 and row['RSI'] < rsi_oversold and cash > row['close']:
            shares_to_buy = cash // row['close']
            shares_owned += shares_to_buy
            cash -= shares_to_buy * row['close']
        # Check for selling opportunity within bearish trend
        elif row['MA_Signal'] == -1 and row['RSI'] > rsi_overbought and shares_owned > 0:
            cash += shares_owned * row['close']
            shares_owned = 0

        # Append current state to lists
        portfolio_values.append(cash + shares_owned * row['close'])
        shares_owned_list.append(shares_owned)

    # Add columns to DataFrame
    df['Portfolio_Value'] = portfolio_values
    df['Shares_Owned'] = shares_owned_list

    return df


if __name__ == '__main__':
    # Define parameters
    symbol = 'BABA'
    start_date = '2021-01-01'
    end_date = '2021-12-31'
    short_window = 10
    long_window = 30
    initial_cash = 10000

    # Run backtest
    df_backtest = backtest(symbol, start_date, end_date, short_window, long_window, initial_cash)

    # # Plot results
    fig, ax1 = plt.subplots(figsize=(14, 7))

    # Plotting the close price
    color = 'tab:red'
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Price', color=color)
    ax1.plot(df_backtest.index, df_backtest['close'], color=color, label='Close Price')
    ax1.tick_params(axis='y', labelcolor=color)

    # Adding a second y-axis for portfolio value
    ax2 = ax1.twinx()
    color = 'tab:blue'
    ax2.set_ylabel('Portfolio Value', color=color)
    ax2.plot(df_backtest.index, df_backtest['Portfolio_Value'], color=color, label='Portfolio Value')
    ax2.tick_params(axis='y', labelcolor=color)

    # Assuming RSI-based buy and sell points are marked in the DataFrame, here's how you might visualize them:
    # For simplicity, let's assume 'Buy_Signal' and 'Sell_Signal' columns exist which mark the RSI condition-based trades
    # This part would need adjustment based on how you're tracking those in your actual DataFrame
    buys = df_backtest[df_backtest['RSI'] < 30]  # Example condition for buys
    sells = df_backtest[df_backtest['RSI'] > 70]  # Example condition for sells

    # Marking buy points with green up arrows
    ax1.scatter(buys.index, buys['close'], color='green', label='Buy Point', marker='^', s=100)
    # Marking sell points with red down arrows
    ax1.scatter(sells.index, sells['close'], color='red', label='Sell Point', marker='v', s=100)

    # Legend and title for clarity
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    plt.title('Backtest Result with RSI-Based Buy/Sell Points')

    plt.show()
    # New plot
    fig, ax1 = plt.subplots(figsize=(14, 7))

    # Plotting the close price
    color = 'tab:red'
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Price', color=color)
    ax1.plot(df_backtest.index, df_backtest['close'], color=color, label='Close Price')
    ax1.tick_params(axis='y', labelcolor=color)

    # Adding a second y-axis for portfolio value
    ax2 = ax1.twinx()
    color = 'tab:blue'
    ax2.set_ylabel('Portfolio Value', color=color)
    ax2.plot(df_backtest.index, df_backtest['Portfolio_Value'], color=color, label='Portfolio Value')
    ax2.tick_params(axis='y', labelcolor=color)

    # Identifying and plotting golden cross and death cross points
    golden_crosses = df_backtest[(df_backtest['Signal'] == 1) & (df_backtest['Signal'].shift(1) != 1)]
    death_crosses = df_backtest[(df_backtest['Signal'] == -1) & (df_backtest['Signal'].shift(1) != -1)]

    # Marking golden crosses with gold stars
    ax1.scatter(golden_crosses.index, golden_crosses['close'], color='gold', label='Golden Cross', marker='*', s=100)
    # Marking death crosses with black stars
    ax1.scatter(death_crosses.index, death_crosses['close'], color='black', label='Death Cross', marker='*', s=100)

    # Explicitly marking buy and sell points
    # Buy points: Assume it's where Signal == 1
    buys = df_backtest[df_backtest['Signal'] == 1]
    # Sell points: Assume it's where Signal == -1
    sells = df_backtest[df_backtest['Signal'] == -1]

    # Marking buy points with green up arrows
    ax1.scatter(buys.index, buys['close'], color='green', label='Buy Point', marker='^', s=100)
    # Marking sell points with red down arrows
    ax1.scatter(sells.index, sells['close'], color='red', label='Sell Point', marker='v', s=100)

    # Legend and title
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    plt.title('Backtest Result with Buy/Sell Points and Crosses')

    plt.show()
