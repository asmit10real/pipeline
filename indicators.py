import pandas as pd
import numpy as np
import logging
import signals as signals

logger = logging.getLogger()
logger.setLevel(logging.CRITICAL) #Debug or Critical are used

#vwap indicator class? trend line indicator class?
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

#window_days = 2 is vwap anchored to yesterday
def AVWAP(df, window_days):
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

def check_trend_line(support: bool, pivot: int, slope: float, y: np.array):
    # compute sum of differences between line and prices, 
    # return negative val if invalid 
    # Find the intercept of the line going through pivot point with given slope
    intercept = -slope * pivot + y[pivot]
    line_vals = slope * np.arange(len(y)) + intercept
    diffs = line_vals - y
    # Check to see if the line is valid, return -1 if it is not valid.
    if support and diffs.max() > 1e-5:
        return -1.0
    elif not support and diffs.min() < -1e-5:
        return -1.0
    # Squared sum of diffs between data and line 
    err = (diffs ** 2.0).sum()
    #logger.warning('Returning check_trend_line()')
    return err;

def optimize_slope(support: bool, pivot:int , init_slope: float, y: np.array):
    # Amount to change slope by. Multiplyed by opt_step
    slope_unit = (y.max() - y.min()) / len(y) 
    # Optmization variables
    opt_step = 1.0
    min_step = 0.0001
    curr_step = opt_step # current step
    # Initiate at the slope of the line of best fit
    best_slope = init_slope
    best_err = check_trend_line(support, pivot, init_slope, y)
    assert(best_err >= 0.0) # Shouldn't ever fail with initial slope
    get_derivative = True
    derivative = None
    while curr_step > min_step:
        if get_derivative:
            # Numerical differentiation, increase slope by very small amount
            # to see if error increases/decreases. 
            # Gives us the direction to change slope.
            slope_change = best_slope + slope_unit * min_step
            test_err = check_trend_line(support, pivot, slope_change, y)
            derivative = test_err - best_err;
            # If increasing by a small amount fails, 
            # try decreasing by a small amount
            if test_err < 0.0:
                slope_change = best_slope - slope_unit * min_step
                test_err = check_trend_line(support, pivot, slope_change, y)
                derivative = best_err - test_err
            if test_err < 0.0: # Derivative failed, give up
                raise Exception("Derivative failed. Check your data. ")
            get_derivative = False
        if derivative > 0.0: # Increasing slope increased error
            test_slope = best_slope - slope_unit * curr_step
        else: # Increasing slope decreased error
            test_slope = best_slope + slope_unit * curr_step
        test_err = check_trend_line(support, pivot, test_slope, y)
        if test_err < 0 or test_err >= best_err: 
            # slope failed/didn't reduce error
            curr_step *= 0.5 # Reduce step size
        else: # test slope reduced error
            best_err = test_err 
            best_slope = test_slope
            get_derivative = True # Recompute derivative
    # Optimize done, return best slope and intercept
    #logger.warning('Returning optimize_slope()')
    return (best_slope, -best_slope * pivot + y[pivot])

def fit_trendlines_single(data: np.array):
    # find line of best fit (least squared) 
    # coefs[0] = slope,  coefs[1] = intercept 
    x = np.arange(len(data))
    coefs = np.polyfit(x, data, 1)
    # Get points of line.
    line_points = coefs[0] * x + coefs[1]
    # Find upper and lower pivot points
    upper_pivot = (data - line_points).argmax() 
    lower_pivot = (data - line_points).argmin() 
    # Optimize the slope for both trend lines
    support_coefs = optimize_slope(True, lower_pivot, coefs[0], data)
    resist_coefs = optimize_slope(False, upper_pivot, coefs[0], data)
    #logger.warning('Returning fit_trendlines_single()')
    return (support_coefs, resist_coefs)

def fit_trendlines_high_low(high: np.array, low: np.array, close: np.array):
    x = np.arange(len(close))
    coefs = np.polyfit(x, close, 1)
    # coefs[0] = slope,  coefs[1] = intercept
    line_points = coefs[0] * x + coefs[1]
    upper_pivot = (high - line_points).argmax() 
    lower_pivot = (low - line_points).argmin() 
    support_coefs = optimize_slope(True, lower_pivot, coefs[0], low)
    resist_coefs = optimize_slope(False, upper_pivot, coefs[0], high)
    #logger.warning('Returning fit_trendlines_high_low()')
    return (support_coefs, resist_coefs)

def getTrend(data: pd.DataFrame, data2: pd.DataFrame, lookback: int, view: int):
        # Take natural log of data to resolve price scaling issues for indicator
        data = np.log(data)
        #Do everything
        logger.warning('Attempting to begin calculating indicator')
        #Calculate indicator
        support_slope = [np.nan] * len(data)
        resist_slope = [np.nan] * len(data)
        for i in range(lookback - 1, len(data)):
            candles = data.iloc[i - lookback + 1: i + 1]
            support_coefs, resist_coefs =  signals.fit_trendlines_high_low(candles['High'], 
                                                                   candles['Low'], 
                                                                   candles['Close'])
            support_slope[i] = support_coefs[0]
            resist_slope[i] = resist_coefs[0]
        
        logger.warning('Attempting to assign indicator values to columnds in data')
        data['support_slope'] = support_slope
        data['resist_slope'] = resist_slope
        v = view * 2
        data['slopeqnt'] = ((data['support_slope'].shift(1) + data['resist_slope'].shift(1)) / 2).rolling(v, min_periods = v).quantile(0.2, interpolation = 'lower')
        #Get results
        data = data.dropna()
        #Get lows and highs of slope in past 30 days excluding today
        data['slopelows'] = data['support_slope'].shift(1).rolling(view, min_periods = view).min()
        data['slopelowr'] = data['resist_slope'].shift(1).rolling(view, min_periods = view).min()
        data['slopehighs'] = data['support_slope'].shift(1).rolling(view, min_periods = view).max()
        data['slopehighr'] = data['resist_slope'].shift(1).rolling(view, min_periods = view).max()
        data = data.dropna()
        #Align datasets
        logger.warning('Attempting to align real and log datasets')
        #logger.critical(data)
        data2 = data2[(data2.index >= data.index[0])]
        data = data.dropna()
        data2 = data2.dropna()
        return data, data2