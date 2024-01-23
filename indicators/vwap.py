import pandas as pd
def VWAP(df: pd.DataFrame):
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