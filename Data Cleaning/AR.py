#first make sure you installed python & package- pip3 install openpyxl

#model used: linear, Labor data = b0+b1*Vol+error

import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt

# Load data
df = pd.read_excel('/Users/tianyishen/Downloads/Civilian Labor Force Participation Rate.xlsx')  # Must contain: 'Month', 'Tether-EUR LogVol', 'Labor data'

# Ensure date is datetime and set index
df['Month'] = pd.to_datetime(df['Month'])
df.set_index('Month', inplace=True)

#_______Tether_____________# - significant, p-value=0.031

# Create lagged log volatility as predictor
df['Lagged_LogVol'] = df['Tether'].shift(1)

# Drop NA (first row will be NaN due to lag)
df = df.dropna()

X = df['Lagged_LogVol']
y = df['Labor data']

X = sm.add_constant(X)

model = sm.OLS(y, X).fit()
print(model.summary())

#_________Bitcoin__________# - not significant, p-value=0.612

# Create lagged log volatility as predictor
df['Lagged_LogVol'] = df['Bitcoin'].shift(1)

# Drop NA (first row will be NaN due to lag)
df = df.dropna()

X = df['Lagged_LogVol']
y = df['Labor data']

X = sm.add_constant(X)

model = sm.OLS(y, X).fit()
print(model.summary())


#_________USD__________# ----significant, p-value=0.025

# Create lagged log volatility as predictor
df['Lagged_LogVol'] = df['USD'].shift(1)

# Drop NA (first row will be NaN due to lag)
df = df.dropna()

X = df['Lagged_LogVol']
y = df['Labor data']

X = sm.add_constant(X)

model = sm.OLS(y, X).fit()
print(model.summary())


#plotting
# Plot all four columns on the same graph
plt.figure(figsize=(12, 6))

# Normalize each series for comparison (optional but recommended)
df_normalized = df[['Labor data', 'Bitcoin', 'USD', 'Tether']].apply(
    lambda x: (x - x.min()) / (x.max() - x.min())
)

# Plot
plt.plot(df_normalized.index, df_normalized['Labor data'], label='Labor Data (normalized)')
plt.plot(df_normalized.index, df_normalized['Bitcoin'], label='Bitcoin (normalized)')
plt.plot(df_normalized.index, df_normalized['USD'], label='USD (normalized)')
plt.plot(df_normalized.index, df_normalized['Tether'], label='Tether (normalized)')

plt.title('Labor Data vs. Crypto Volatility & USD (2017–2025)')
plt.xlabel('Date')
plt.ylabel('Normalized Value')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
