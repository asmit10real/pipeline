import pandas as pd
import logging

logger = logging.getLogger()
logger.setLevel(logging.CRITICAL) #Debug or Critical are used

def calc(df: pd.DataFrame):
    threshold_date = df.index[0] + pd.Timedelta(days=14)
    df['cummax'] = df.loc[:,'cumreturns'].cummax()
    df['cummaxstrat'] = df.loc[:,'cumreturnsstrat'].cummax()
    df['roll_max'] = df['Close'].cummax()
    df['dailyDraw'] = (df['Close'] - df['roll_max']) / df['roll_max'] * 100
    df['maxDailyDrawdown'] = df['dailyDraw'].cummin()
    df['drawdownstrat'] = ((df['equitycurve'] - df['peakcurve']) / df['peakcurve']) * 100
    df['drawmaxstrat'] = df.loc[:,'drawdownstrat'].cummin()
    df = df.dropna()
    return df

def output(df: pd.DataFrame):
    df = df.copy()
    maxdraw = df['drawmax'][-1]
    maxprofit = df['cummax'][-1]
    maxdrawstrat = df['drawmaxstrat'][-1]
    maxprofitstrat = df['cummaxstrat'][-1]
    print(f"Max Draw HOLDING: {maxdraw} Max Draw STRAT: {maxdrawstrat}")
    print(f"Max Profit HOLDING: {maxprofit} Max Profit STRAT: {maxprofitstrat}")
    print(basePerf(df, 252))
    print(basePerf(df, 252, strategy = True))

def basePerf(df: pd.DataFrame, n_bars_in_year = 252, strategy = False, multiple = False):
    logger.warning('Attempting to calc baseperf')
    df = df.copy()
    if(strategy):
        r = df['Strategy']
    else:
        r = df['Returnsb&h']
    #Compute performance metrics
    profit_factor = r[r > 0].sum() / r[r < 0].abs().sum()
    sharpe = r.mean() / r.std()
    sortino = r.mean() / (r[r < 0].std())
    # Annualize sharpe and sortino ratio
    sharpe *= n_bars_in_year ** 0.5
    sortino *= n_bars_in_year ** 0.5
    return {"Profit Factor": profit_factor, "Sharpe Ratio": sharpe, "Sortino Ratio": sortino}