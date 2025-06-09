#takes in excel file from data with log return of either tether or data
#generates an excel with monthly volatility for tether or data as a column, with date
#generates excel with monthly price of VIX
#edited June 5, 2025

import pandas as pd
import numpy as np

def compute_monthly_log_volatility(df, date_col='Date', return_col='Log Return'):
    """
    Compute monthly log volatility from daily log returns using the realized volatility method.

    Parameters:
    - df: DataFrame with daily log returns and dates.
    - date_col: Name of the date column.
    - return_col: Name of the log return column.

    Returns:
    - DataFrame with columns: ['Month', 'Log Volatility']
    """

    # Ensure date column is datetime
    df[date_col] = pd.to_datetime(df[date_col])

    # Drop NA returns and sort
    df = df[[date_col, return_col]].dropna().sort_values(date_col).copy()

    # Create 'Month' column as period
    df['Month'] = df[date_col].dt.to_period('M')

    # Square the returns
    df['Squared Return'] = df[return_col] ** 2

    # Group by month, sum squared returns
    monthly_vol = df.groupby('Month').agg({
        'Squared Return': 'sum',
        date_col: 'last'  # Last trading day of the month
    }).reset_index()

    # Compute log volatility
    monthly_vol['Log Volatility'] = np.log(np.sqrt(monthly_vol['Squared Return']))

    # Optional: rename columns
    monthly_vol = monthly_vol.rename(columns={date_col: 'Month End Date'})

    return monthly_vol[['Month', 'Month End Date', 'Log Volatility']]


def get_end_of_month_values(df, date_col='DATE', price_col='CLOSE'):
    """
    Extracts end-of-month values from a daily time series.

    Parameters:
    - df: DataFrame with daily data.
    - date_col: Name of the column containing dates.
    - price_col: Name of the column containing the price/indicator value (e.g., VIX, MOVE).

    Returns:
    - DataFrame with columns: ['Month', 'Month End Date', 'EOM Value']
    """

    # Ensure datetime format and sort
    df[date_col] = pd.to_datetime(df[date_col])
    df = df.sort_values(by=date_col).dropna(subset=[price_col]).copy()

    # Add period
    df['Month'] = df[date_col].dt.to_period('M')

    # Find the last trading date of each month
    eom_dates = df.groupby('Month')[date_col].max().reset_index()

    # Merge to get EOM value
    eom_values = pd.merge(eom_dates, df[[date_col, price_col]], on=date_col, how='left')
    eom_values = eom_values.rename(columns={
        date_col: 'Month End Date',
        price_col: 'EOM Value'
    })

    return eom_values[['Month', 'Month End Date', 'EOM Value']]


# --- Example usage ---
if __name__ == "__main__":

###############################################################################
#For Tether & Bitcoin
##if you want to do bitcoin, switch to bitcoin## this is generating tether to data
###############################################################################

    # Load excel
    df=pd.read_excel('/Users/tianyishen/Desktop/BTC, Tether Log Volatility For Extraction.xlsx')

    print(df.head)

    # Compute monthly log volatility
    result = compute_monthly_log_volatility(df)

    # Save or print
    print(result.head())
    result.to_excel('/Users/tianyishen/Desktop/USD_Coin_LastOfMonth.xlsx', index=False)

# ###############################################################################
# #For VIX & MOVE

#     vix_df =pd.read_excel('data/VIX.xlsx')
#     # Assume vix_df and move_df are loaded with columns: Date, Value

#     vix_eom = get_end_of_month_values(vix_df, date_col='DATE', price_col='CLOSE')
#     # move_eom = get_end_of_month_values(move_df, date_col='Date', price_col='MOVE')

#     print(vix_eom.head())
#     vix_eom.to_excel('data/VIX_LastOfMonth.xlsx', index=False)
