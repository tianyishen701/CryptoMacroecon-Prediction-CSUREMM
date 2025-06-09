#calculates volatility from investing.com csv for currency vars

import pandas as pd
import numpy as np
import os

def compute_daily_log_return(df, date_col='Date', price_col='Close'):
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    df = df.sort_values(by=date_col)
    df['Log Return'] = np.log(df[price_col] / df[price_col].shift(1))
    return df[[date_col, 'Log Return']]

def compute_monthly_log_volatility(df, date_col='Date', return_col='Log Return'):
    df[date_col] = pd.to_datetime(df[date_col])
    df = df.dropna(subset=[return_col]).copy()
    df['Month'] = df[date_col].dt.to_period('M')
    df['Squared Return'] = df[return_col] ** 2
    monthly_vol = df.groupby('Month').agg({
        'Squared Return': 'sum',
        date_col: 'last'
    }).reset_index()
    monthly_vol['Log Volatility'] = np.log(np.sqrt(monthly_vol['Squared Return']))
    monthly_vol = monthly_vol.rename(columns={date_col: 'Month End Date'})
    return monthly_vol[['Month', 'Month End Date', 'Log Volatility']]

def get_end_of_month_prices(df, date_col='Date', price_col='Close'):
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    df = df.sort_values(by=date_col)
    df['Month'] = df[date_col].dt.to_period('M')
    eom_dates = df.groupby('Month')[date_col].max().reset_index()
    eom_prices = pd.merge(eom_dates, df[[date_col, price_col]], on=date_col, how='left')
    eom_prices = eom_prices.rename(columns={date_col: 'Month End Date', price_col: 'EOM Price'})
    return eom_prices[['Month', 'Month End Date', 'EOM Price']]

# --- Main execution ---
if __name__ == "__main__":
    # Load your dataset (choose Litecoin or XRP)
    file_path = '/Users/tianyishen/Downloads/Litecoin Historical Data.csv'  # <- You can also use 'XRP Historical Data.csv', change this to whatever path name
    df = pd.read_csv(file_path)
    df['Date'] = pd.to_datetime(df['Date'])


    # Clean columns for standard naming
    df.columns = [col.strip().replace(' ', '_') for col in df.columns]
    df = df.rename(columns={'Date': 'Date', 'Price': 'Close'})  # Use 'Close' as normalized column name

    # Remove commas and convert to float
    df['Close'] = df['Close'].replace(',', '', regex=True).astype(float)

    # Calculate daily log returns
    df_log_returns = compute_daily_log_return(df, date_col='Date', price_col='Close')

    # Join with original dates to compute monthly volatility
    df_returns_merged = df[['Date']].merge(df_log_returns, on='Date', how='left')

    # Compute monthly log volatility
    monthly_vol = compute_monthly_log_volatility(df_returns_merged)

    # Get monthly EOM price
    eom_prices = get_end_of_month_prices(df, date_col='Date', price_col='Close')

    # Output Excel
    asset_name = os.path.splitext(os.path.basename(file_path))[0].replace(' ', '_')
    monthly_vol.to_excel(f'{asset_name}_Monthly_LogVol.xlsx', index=False)
    eom_prices.to_excel(f'{asset_name}_Monthly_EOM_Price.xlsx', index=False)

    print(monthly_vol.head())
    print(eom_prices.head())
