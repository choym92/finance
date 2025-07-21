# 사용자가 제시한 전략(RSI 및 MACD 기반)을 이용한 아마존(AMZN)의 주가 데이터를 활용한 백테스팅을 수행하겠습니다.
# Yahoo Finance에서 AMZN 주가 데이터를 불러온 후, RSI 및 MACD 지표 기반의 간단한 자동매매 전략을 구현하고 성과를 시뮬레이션합니다.

import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import pandas_ta as ta

# 데이터 로딩 (최근 2년간)
ticker = "AMZN"
df = yf.download(ticker, start="2023-05-01", end="2025-05-01")

# RSI, MACD 계산
df['RSI'] = ta.rsi(df['Close'], length=14)
macd = ta.macd(df['Close'])
df = pd.concat([df, macd], axis=1)

# 매매 전략 조건 설정
# 매수: MACD 골든 크로스 (MACD > Signal) & RSI < 40 (과매도에서 상승 전환)
# 매도: MACD 데드 크로스 (MACD < Signal) & RSI > 60 (과매수에서 하락 전환)

df['Buy_Signal'] = np.where((df['MACD_12_26_9'] > df['MACDs_12_26_9']) & (df['RSI'] < 40), 1, 0)
df['Sell_Signal'] = np.where((df['MACD_12_26_9'] < df['MACDs_12_26_9']) & (df['RSI'] > 60), -1, 0)

# 포지션 관리
df['Position'] = df['Buy_Signal'] + df['Sell_Signal']
df['Position'] = df['Position'].replace(to_replace=0, method='ffill').fillna(0)

# 전략 수익률 계산
df['Strategy_Return'] = df['Close'].pct_change() * df['Position'].shift(1)

# 누적 수익률 계산
df['Cumulative_Strategy_Return'] = (1 + df['Strategy_Return']).cumprod()
df['Cumulative_Market_Return'] = (1 + df['Close'].pct_change()).cumprod()

# 성과 시각화
plt.figure(figsize=(12, 6))
plt.plot(df['Cumulative_Strategy_Return'], label='RSI & MACD Strategy Return')
plt.plot(df['Cumulative_Market_Return'], label='AMZN Market Return', linestyle='--')
plt.title('Backtesting: RSI & MACD Strategy vs. AMZN Market Return')
plt.xlabel('Date')
plt.ylabel('Cumulative Return')
plt.legend()
plt.grid(True)
plt.show()

# 최종 성과 요약
final_strategy_return = df['Cumulative_Strategy_Return'].iloc[-1]
final_market_return = df['Cumulative_Market_Return'].iloc[-1]

final_strategy_return, final_market_return
