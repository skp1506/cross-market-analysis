# 📊 Cross-Market Analysis: Crypto, Oil & Stocks

A SQL-powered Streamlit dashboard for analyzing and comparing
cryptocurrency, crude oil, and stock market data.

##  Project Overview

This project performs cross-market analysis between:

- Cryptocurrency
- WTI Crude Oil
- S&P 500
- NASDAQ
- NIFTY

The application uses SQL queries and Streamlit to explore market
trends, prices, and relationships between different financial assets.

##  Technologies Used

- Python
- SQL
- MySQL
- Pandas
- Streamlit
- CoinGecko API
- Yahoo Finance API

##  Key Features

### 1. Cross-Market Overview

- Select a date range
- Calculate average Bitcoin price
- Calculate average oil price
- Calculate average S&P 500 closing price
- Calculate average NIFTY closing price
- Display a daily market snapshot

### 2. SQL Query Runner

- Select predefined SQL queries
- Execute SQL queries through Streamlit
- Display query results in table format
- Perform SQL-based market analysis

### 3. Crypto Analysis

- Select cryptocurrency
- Apply date filters
- View daily cryptocurrency prices
- Analyze cryptocurrency price trends

##  Project Files

| File | Description |
|------|-------------|
| `app.py` | Main Streamlit application |
| `Market Analysis.ipynb` | Data analysis notebook |
| `crypto_data.csv` | Cryptocurrency dataset |
| `oil_price.csv` | WTI oil price dataset |
| `stocks_price.csv` | Stock market dataset |
| `top 3 coin_history.csv` | Historical prices of top cryptocurrencies |
| `requirements.txt` | Python dependencies |
| `.gitignore` | Files excluded from Git |

##  Database

The project uses MySQL for storing and analyzing market data.

The database contains market-related tables for:

- Cryptocurrencies
- Crypto prices
- Oil prices
- Stock prices

##  SQL Analysis

The project includes SQL analysis such as:

- Top cryptocurrencies by market capitalization
- Average cryptocurrency prices
- Highest and lowest oil prices
- Stock market price analysis
- Monthly average closing prices
- Cross-market comparisons
- Bitcoin vs oil analysis
- Bitcoin vs S&P 500 analysis
- Crypto vs stock market comparisons

##  How to Run

### 1. Clone the repository

```bash
git clone https://github.com/skp1506/cross-market-analysis.git
cd cross-market-analysis