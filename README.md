# Indian Stock Market Dashboard (2020-2024)

An end-to-end data science project covering data collection, SQL storage, 
analysis, and an interactive Streamlit dashboard.

## What this project does

- Pulls 5 years of daily closing prices for 15 NIFTY 50 stocks using yfinance
- Stores data in a SQLite database and queries it with SQL
- Analyses 5-year returns, volatility, moving averages, and stock correlations
- Presents everything in an interactive Streamlit dashboard

## Key findings

- Adani Enterprises gave 1127% return but with 54% annual volatility — highest risk
- L&T, Infosys, and Titan quietly doubled with relatively low risk
- Kotak Bank gave only 7% over 5 years — barely above inflation
- TCS and HUL showed the lowest correlation with other stocks — best diversifiers

## Tech stack

Python, pandas, yfinance, SQLite, SQL, matplotlib, Streamlit

## How to run

```bash
pip install yfinance streamlit matplotlib pandas
streamlit run stock_dashboard.py
```

## Dashboard preview

Select any stock from the sidebar to see its price trend, moving averages, 
5-year return, and volatility metrics.
