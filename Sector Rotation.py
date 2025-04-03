import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# ETFs and labels
etfs = ['XLK', 'XLF', 'XLV', 'XLE', 'XLI']
labels = ['Technology', 'Financials', 'Healthcare', 'Energy', 'Industrials']

# Download data
data = yf.download(etfs, start="2020-01-01", end="2024-12-31", interval="1mo", group_by='ticker', auto_adjust=True)

# Build a new DataFrame for adjusted close prices
adj_close = pd.DataFrame()

for symbol, label in zip(etfs, labels):
    try:
        adj_close[label] = data[symbol]['Close']
    except KeyError:
        print(f"Data for {symbol} not found.")

# Drop rows with missing values
adj_close.dropna(inplace=True)

# Monthly returns
monthly_returns = adj_close.pct_change().dropna()

# Sector rotation logic
portfolio_value = 100
portfolio = []
dates = []

for i in range(1, len(monthly_returns)):
    last_month = monthly_returns.iloc[i - 1]
    top_sector = last_month.idxmax()
    next_return = monthly_returns.iloc[i][top_sector]
    portfolio_value *= (1 + next_return)
    portfolio.append(portfolio_value)
    dates.append(monthly_returns.index[i])

# Equal-weighted benchmark
benchmark = (monthly_returns + 1).cumprod().mean(axis=1) * 100

# Plot
plt.figure(figsize=(12, 6))
plt.plot(dates, portfolio, label="Sector Rotation Strategy", linewidth=2)
plt.plot(benchmark.index, benchmark.values, linestyle='--', label="Equal-Weighted Benchmark")
plt.title("Sector Rotation vs. Equal-Weighted Strategy")
plt.xlabel("Date")
plt.ylabel("Portfolio Value ($)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

