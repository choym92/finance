import requests, json
from api_keys import *


BASE_URL = 'https://paper-api.alpaca.markets'
ACCOUNT_URL = f"{BASE_URL}/v2/account"
ORDERS_URL = f"{BASE_URL}/v2/orders"
HEADERS = {'APCA-API-KEY-ID': ALPACA_TRADER_API_KEY, 'APCA-API-SECRET-KEY': ALPACA_TRADER_API_SECRET}

def get_account():
    r = requests.get(ACCOUNT_URL, headers=HEADERS)
    return json.loads(r.content)

def create_order(symbol, qty, side, type, time_inforce ):
    data = {
        "symbol": symbol,
        "qty": qty,
        "side": side,
        "type": type,
        "time_inforce": time_inforce
    }
    r = requests.post(ORDERS_URL, json=data, headers=HEADERS)
    return json.loads(r.content)

def get_orders():
    r = requests.get(ACCOUNT_URL, headers=HEADERS)
    return json.loads(r.content)

orders = get_orders()
print(orders)

response = create_order("AAPL", 1, "buy", "market", 'gtc')
print(response)



from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetAssetsRequest
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

trading_client = TradingClient(ALPACA_TRADER_API_KEY, ALPACA_TRADER_API_SECRET)


# Get our account information.
account = trading_client.get_account()

# Check if our account is restricted from trading.
if account.trading_blocked:
    print('Account is currently restricted from trading.')

# Check how much money we can use to open new positions.
print('${} is available as buying power.'.format(account.buying_power))

# Check our current balance vs. our balance at the last market close
balance_change = float(account.equity) - float(account.last_equity)
print(f'Today\'s portfolio balance change: ${balance_change}')

# preparing market order
market_order_data = MarketOrderRequest(
                    symbol="SPY",
                    qty=1,
                    side=OrderSide.BUY,
                    time_in_force=TimeInForce.DAY
                    )

# preparing orders
market_order_data = MarketOrderRequest(
                    symbol="SPY",
                    qty=1,
                    side=OrderSide.SELL,
                    time_in_force=TimeInForce.GTC
                    )

# Market order
market_order = trading_client.submit_order(
                order_data=market_order_data
               )
