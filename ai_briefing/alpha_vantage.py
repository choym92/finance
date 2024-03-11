import requests
from api_keys import ALPHA_VANTAGE_API_KEY

url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers=AAPL&apikey={ALPHA_VANTAGE_API_KEY}'
r = requests.get(url)
data = r.json()

print(data)



url = f'https://www.alphavantage.co/query?function=REAL_GDP&interval=quarterly&apikey={ALPHA_VANTAGE_API_KEY}'
r = requests.get(url)
gdp = r.json()

print(gdp)


# Market Sentiment, Economic Growth Prospects, Monetary Policy Outlook, Inflation Expectations
MATURITY = '10year'
INTERVAL = 'weekly'
url = f'https://www.alphavantage.co/query?function=TREASURY_YIELD&interval={INTERVAL}&maturity={MATURITY}&apikey={ALPHA_VANTAGE_API_KEY}'
r = requests.get(url)
treasuery_yield = r.json()

print(treasuery_yield)