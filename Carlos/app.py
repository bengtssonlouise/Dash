import pandas as pd

# Load data
df = pd.read_csv('data/stockdata2.csv'. index_col=2, parse_dates=True)
df.index = pd.to_datetime(df['Date'])

print(df.head())