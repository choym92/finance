import requests
import pandas as pd
import datetime
from alpha_vantage.timeseries import TimeSeries

API_KEY = 'ATBQ17CSM645CQ6Z'
SYMBOL = 'SPY'
DATE_RANGE = '2022-11-02T14:31:15&RANGE=2022-11-02T15:16:25'
INTERVAL = '5min'
OHLC = 'close'
url = f'https://alphavantageapi.co/timeseries/analytics?SYMBOLS={SYMBOL}&RANGE={DATE_RANGE}&INTERVAL={INTERVAL}&' \
      f'OHLC=close&CALCULATIONS=MIN,MAX,MEAN,STDDEV,CORRELATION&apikey={API_KEY}'

r = requests.get(url)
data = r.json()

print(data)

# RANGE=2020-12-01T00:04:00&RANGE=2020-12-06T23:59:59

# Initialize AlphaVantage TimeSeries object
ts = TimeSeries(key=API_KEY, output_format='pandas')
ts.get_daily_adjusted()
# Specify the symbol and other parameters
symbol = 'SPY'
interval = '5min'  # Adjust the interval as per your requirement

# Define start and end times
powell_start_time = "2022-11-02 14:31:15"
powell_end_time = "2022-11-02 15:16:25"
start = datetime.datetime.strptime(powell_start_time, '%Y-%m-%d %H:%M:%S')
end = datetime.datetime.strptime(powell_end_time, '%Y-%m-%d %H:%M:%S')
ts.get_daily()
# Request historical data
data, meta_data = ts.get_intraday(symbol=symbol, interval=interval, outputsize='full')

# Filter data for the required time range
df = data.loc[start:end]

# Save data to CSV
df.to_csv(symbol + '.csv')







import pandas as pd
from alpha_vantage.timeseries import TimeSeries

# Set up AlphaVantage API key
api_key = 'YOUR_API_KEY'  # Replace 'YOUR_API_KEY' with your actual API key

# Initialize AlphaVantage TimeSeries object
ts = TimeSeries(key=api_key, output_format='pandas')

# Specify the symbol and other parameters
symbol = 'SPY'
interval = '5min'  # Adjust the interval as per your requirement

# Define start and end times
powell_start_time = "2022-11-02 14:31:15"
powell_end_time = "2022-11-02 15:16:25"

# Request historical data
data, meta_data = ts.get_intraday(symbol=symbol, outputsize='full')

# Filter data for the required time range
start_index = data.index.searchsorted(powell_start_time)
end_index = data.index.searchsorted(powell_end_time)
df = data.iloc[start_index:end_index]

# Save data to CSV
df.to_csv(symbol + '_alphavantage.csv')


