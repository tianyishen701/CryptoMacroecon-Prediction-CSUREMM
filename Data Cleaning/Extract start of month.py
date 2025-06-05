##original extraction file, no longer used

import pandas as pd

# Load your data (adjust path to your actual file)
df = pd.read_excel('/Users/tianyishen/Downloads/SampleRealVolCalculation (1).xlsx')

# Ensure 'Date' is datetime
df['Date'] = pd.to_datetime(df['Date'])

# Sort by date (if not already)
df = df.sort_values('Date')

# Filter starting from September 2017
df = df[df['Date'] >= '2017-09-01']

# Create Year-Month column
df['YearMonth'] = df['Date'].dt.to_period('M')

# Select first row of each month (first trading day)
first_days = df.groupby('YearMonth').first().reset_index()

# Extract relevant columns
result = first_days[['Date', 'Log VOL']]

# save & view result
print(result)
result.to_excel('/Users/tianyishen/Desktop/Bitcoin_FirstOfMonth.xlsx', index=False)
