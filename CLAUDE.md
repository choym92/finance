# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based financial analysis and trading system with multiple components:

- **AI Financial Briefing**: Automated news scraping and analysis using NewsAPI and FinViz
- **Trading & Backtesting**: Alpaca API integration for paper trading and strategy backtesting
- **Data Analysis**: Financial data retrieval from various sources (Yahoo Finance, Alpha Vantage)
- **RAG System**: Document analysis system for financial reports using OpenAI

## Setup and Dependencies

### Environment Setup
- Install dependencies: `pip install -r requirements.txt`
- The project uses a virtual environment at `finance-ai/`
- API keys are managed through `.env` file (not tracked in git) and `api_keys.py`

### Required API Keys
Configure these in your `.env` file:
- `NEWS_API_KEY`: For news scraping via NewsAPI
- `ALPACA_TRADER_API_KEY` & `ALPACA_TRADER_API_SECRET`: For Alpaca trading (in api_keys.py)
- OpenAI API key: Set in `ai_briefing/RAG/rag.py`

## Architecture

### Core Components

1. **AI Briefing System** (`ai_briefing/`)
   - `main.py`: Primary orchestration script combining news sources
   - `scrapers/`: News data collection from multiple sources
     - `get_news.py`: NewsAPI integration with financial domain filtering
     - `fear_greed_index.py`: Sentiment indicator scraping
     - `youtube_transcript.py`: Financial video content analysis
   - `RAG/`: Document analysis system for 10-K reports and PDFs

2. **Trading System**
   - `alapca_trade.py`: Live Alpaca API trading client
   - `backtest.py`: Strategy backtesting with RSI and moving average signals
   - Uses paper trading environment by default (`https://paper-api.alpaca.markets`)

3. **Data Sources**
   - `yahoo.py`: Yahoo Finance integration
   - `get_price_data.py`: Historical price data retrieval
   - `alpha_vantage.py`: Alpha Vantage API wrapper

### Data Flow
1. News scraping aggregates data from NewsAPI and FinViz
2. Data preprocessing combines and cleans multiple sources
3. Analysis pipeline processes financial metrics and sentiment
4. Trading decisions can be executed via Alpaca API or backtested

## Important Implementation Notes

### Path Configuration
- `ai_briefing/main.py` contains hardcoded Windows path: `C:\\Users\\Paul Cho\\Documents\\YM\\Project\\finance`
- Update this path when working on different systems

### Data Storage
- News data saved to `src/data/news_{date}.csv`
- Historical price data in `src/data/spy.csv`
- RAG system processes PDFs from `ai_briefing/RAG/data/10k/`

### Trading Configuration
- Default symbol for backtesting: BABA
- Default backtesting period: 2021 (full year)
- RSI parameters: 14-period, oversold=30, overbought=70
- Moving averages: 10-day short, 30-day long

### Security Considerations
- API keys are loaded from `.env` and `api_keys.py` (not in version control)
- Uses paper trading by default for safety
- OpenAI API key is hardcoded in RAG module (should be moved to env vars)

## Development Workflow

When working with this codebase:
1. Ensure API keys are properly configured
2. Use the virtual environment: `source finance-ai/bin/activate`
3. Test with paper trading before any live trading modifications
4. Update hardcoded paths for cross-platform compatibility
5. News data is date-stamped and saved automatically