import pandas as pd

def calcVWAP(df: pd.DataFrame):
    # Calculate OHLC/4 for each period
    df['AveragePrice'] = (df['Open'] + df['Close'] + df['High'] + df['Low']) / 4

    # Ensure that 'Date' is a datetime type and group by date
    #df['Date'] = pd.to_datetime(df.loc[:, 'Date']).dt.date
    VWAP = df.groupby(df.index).apply(
        lambda x: (x['AveragePrice'] * x['Volume']).cumsum() / x['Volume'].cumsum()
    )

    # Reset the index to match the original DataFrame's structure
    VWAP = VWAP.reset_index(level=0, drop=True)
    
    return VWAP

#window_days = 2 is vwap anchored to yesterday
def calcAVWAP(df, window_days):
    """
    Calculate Anchored VWAP using a rolling window approach.

    Parameters:
    df (pd.DataFrame): DataFrame with columns 'Open', 'High', 'Low', 'Close', 'Volume'.
    window_days (int): Number of days to look back for the AVWAP calculation.

    Returns:
    pd.Series: Anchored VWAP values.
    """
    # Calculate OHLC/4 for each period
    df['AveragePrice'] = (df['Open'] + df['Close'] + df['High'] + df['Low']) / 4

    # Calculate rolling cumulative price-volume and rolling cumulative volume
    rolling_pv = df['AveragePrice'] * df['Volume']
    rolling_cum_pv = rolling_pv.rolling(window=window_days, min_periods=1).sum()
    rolling_cum_volume = df['Volume'].rolling(window=window_days, min_periods=1).sum()

    # Calculate AVWAP
    AVWAP = rolling_cum_pv / rolling_cum_volume

    return AVWAP