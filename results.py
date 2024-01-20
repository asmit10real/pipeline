import pandas as pd
import logging
import sqlite3
import numpy as np
import yfinance as yf
import performance as perf
import sql as sql
import signals as signals
import indicators as indicators
#Plots
import matplotlib
matplotlib.use('Qt5Agg')  # or 'TkAgg', 'GTK3Agg', etc.
import matplotlib.pyplot as plt
logger = logging.getLogger()
logger.setLevel(logging.CRITICAL) #Debug or Critical are used

def processData(df: pd.DataFrame):
    logger.warning('Attempting to processData() df = df.copy()')
    df = df.copy()
    logger.warning('Setting maxdraw maxprofit maxdrawstrat maxprofitstrat to df[x][-1]')
    #maxDailyDrawdown
    maxdraw = df['maxDailyDrawdown'][-1]
    maxprofit = df['cummax'][-1]
    maxdrawstrat = df['drawmaxstrat'][-1]
    maxprofitstrat = df['cummaxstrat'][-1]
    logger.warning('Attempting to calculate basePerf() for buy and hold')
    holdres = perf.basePerf(df, 252)
    logger.warning('Attempting to calculate basePerf() for strategy')
    stratres = perf.basePerf(df, 252, strategy = True)
    return holdres, stratres

#Pass raw data | lookback is an indicator variable. View is a strategy variable
def processDataMultiple(stocks: list, dateFrom: str, dateTO: str, lookback: int, view: int, strat = 1, plotMe = True):
    indx = 1
    d1 = dateFrom.replace('-', "")
    d2 = dateTO.replace('-', "")
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('stock_data.db')
    connRaw = sqlite3.connect('raw_data.db')
    #Naive implementation
    #sql.getData(stock: str, start_date: str, end_date: str, conn) -> pd.DataFrame:
    for stock in stocks:
        #logger.critical("Checking if data is already downloaded")
        debug = sql.exists(stock, dateFrom, dateTO, connRaw)
        logger.critical(f'TRUE/FALSE EVALS TO: {debug}')
        if(sql.exists(stock, dateFrom, dateTO, connRaw) == False):
            #Data isn't downloaded, downloading it
            #logger.critical("Data isn't downloaded, downloading it")
            data = yf.download(stock, dateFrom, dateTO)
            #Formatting
            data.rename(columns={'Adj Close': 'AdjClose'}, inplace=True)
            data.reset_index(inplace=True) # Resetting index if date is index
            data.loc[:, 'Date'] = pd.to_datetime(data.loc[:, 'Date']).dt.strftime('%Y-%m-%d') # Format date
            # Writing it
            #Writing it
            debug = data.iloc[:, 0]
            try:
                #logger.critical("Attempting to write data")
                #logger.critical(debug)
                sql.writeRaw(data, stock)
            except:
                logger.warning("Fuck")
    logger.warning("MOVING ON")
    
    #END OF NAIVE
    logger.warning('Attempting to processDataMultiple()')
    logger.warning('Create ans as empty data frame')
    ans = pd.DataFrame()
    logger.warning('Beginning loop through stocks')
    axs = []
    plots = []
    for stock in stocks:
        logger.warning(f'Attempting to work on {stock}')
        #dl data
        logger.warning('Attempting to download data')
        data = sql.getData(stock, dateFrom, dateTO, connRaw)
        debug = data.columns
        logger.critical(debug)
        data['VWAP'] = signals.calcVWAP(data)
        data['AVWAP'] = signals.calcAVWAP(data, 2)
        #logger.critical(data['VWAP'])
        #logger.critical(data['AVWAP'])
        #logger.critical(f'DATA FROM sql.getData {data}')
        #data.loc[:, 'Date'] = pd.to_datetime(data.loc[:, 'Date'])
        #data.set_index('Date', inplace=True)
        #logger.critical(data['Close'])
        #Input raw into db if not there
        #sql.writeRaw(data, sto)
        #End db code
        #setup
        logger.warning('Creating copy of data called data2 for real pricing performance calculations')
        #Save copy of data for real pricing for performance calcs
        data2 = data.copy()
        # Take natural log of data to resolve price scaling issues for indicator
        data = np.log(data)

        data, data2 = indicators.getTrend(data, data2, lookback, view)
        #Assign position based on signals.signal(s) np.where(signal1 + signal2 = 2, 1, 0)
        logger.warning('Attempting to set position based on data')
        #STRATEGY
        #CHANGE THIS TO CHANGE STRATEGY
        #logger.critical(f'STUFF: {signals.signal(data, strat)[1]}')
        data2.loc[:,'position'] = signals.signal(data, strat)[0]
        data.loc[:,'position'] = signals.signal(data, strat)[0]
        #Calculate buy and hold returns for raw data and log data
        logger.warning('Attempting to set Buy and hold returns')
        data['Returnsb&h'] = data.loc[:,'Close'] - data.loc[:,'Close'].shift(1)
        data2['Returnsb&h'] = data2.loc[:,'Close'].pct_change()
        #Calculate strategy returns based on position for both log and real
        logger.warning('Attempting to set strategy returns based on position')
        data['Strategy'] = data.loc[:,'Returnsb&h'] * data.loc[:,'position'].shift(1)
        data2['Strategy'] = data2.loc[:,'Returnsb&h'] * data2.loc[:,'position'].shift(1)
        #Drop nans
        logger.warning('Attempting to drop NaNs')
        data2 = data2.dropna()
        data = data.dropna()
        #Calculate cumulative compounding returns for buying and holding along with our strategy
        # * 100 to make it a %
        logger.warning('Attempting to set cumreturns for strat and hold for both log and real')
        data2['cumreturns'] = ((1 + data2.loc[:,'Returnsb&h']).cumprod() - 1) * 100
        data2['cumreturnsstrat'] = ((1 + data2.loc[:,'Strategy']).cumprod() - 1) * 100
        data['cumreturns'] = ((1 + data.loc[:,'Returnsb&h']).cumprod() - 1) * 100
        data['cumreturnsstrat'] = ((1 + data.loc[:,'Strategy']).cumprod() - 1) * 100
        #Equity Curve
        data2['equitycurve'] = 100 * (1 + data2.loc[:,'cumreturnsstrat'] / 100)
        data['equitycurve'] = 100 * (1 + data.loc[:,'cumreturnsstrat'] / 100)
        data2['peakcurve'] = data2['equitycurve'].cummax()
        data['peakcurve'] = data['equitycurve'].cummax()
        logger.warning('Attempting to drop NaNs')
        data2 = data2.dropna()
        data = data.dropna()
        #Moved to function
        logger.warning('Calling calcData on data2')
        data2 = perf.calc(data2)
        #data2.head()
        logger.warning('Attempting to drop NaNs from data2')
        data2 = data2.dropna()
        logger.warning('Attempting to set z to processData(data2) (real pricing)')
        z = processData(data2)
        dx = {
            "Max Drawdown" : [data2['maxDailyDrawdown'][-1], data2['drawmaxstrat'][-1]],
            "Max Profit" : [data2['cummax'][-1], data2['cummaxstrat'][-1]]
        }
        res2 = pd.DataFrame(dx)
        bug = data.head()
        #logger.critical(f'data: {bug}')
        dz = {
            "Num Positions" : [1, signals.signal(data, strat)[1]],
            "PnL" : [(1 + data2['cumreturns'][-1] / 100), (1 + data2.loc[:,'cumreturnsstrat'][-1] / 100)]
        }
        #logger.critical(f'DZ DZ:{dz}')
        res3 = pd.DataFrame(dz)
        #0 = hold 1 = strat
        logger.warning('Attempting to set a new dataFrame res to pd.DataFrame(z) where z is results')
        res1 = pd.DataFrame(z)
        res = pd.concat([res2, res1], axis = 1)
        res = pd.concat([res, res3], axis = 1)
        logger.warning('Attempting to concatanate ans along with res')
        ans = pd.concat([ans, res], axis = 0)
        logger.warning('Attempting to plot slopes and pos')
        plt.style.use('dark_background')
        indx += 2
        # Create a new figure for each stock with a 2x2 grid of subplots
        if(plotMe):
            logger.warning('Attempting to plot things')
            fig, axs = plt.subplots(2, 2, figsize=(24, 16))
            axs = axs.flatten()  # Flatten the array for easier indexing
            data['support_slope'].plot(ax = axs[0], figsize=(24,16), title=f"{stock} SLOPES", label='Support Slope', color='green', legend = True)
            data['resist_slope'].plot(ax = axs[0], label='Resistance Slope', color='red', legend = True)
            data2['position'].plot(ax = axs[0], label='position', color='white', legend = True, secondary_y= True)

            data2['Close'].plot(ax = axs[1], figsize=(24, 16), title=f"{stock} Close", label='Close', color='blue', legend = True)  
            data2['position'].plot(ax = axs[1], label='position', color='white', legend = True, secondary_y= True)

            data2['maxDailyDrawdown'].plot(ax = axs[2], figsize=(24,16), title=f"DRAWDOWN B&H vs Strategy {stock}", fontsize=12, legend = True)
            data2['drawmaxstrat'].plot(ax = axs[2], legend = True)

            data2['equitycurve'].plot(ax = axs[3], figsize=(24,16), title=f"Strategy Equity curve vs B&H curve {stock}", fontsize=12, legend = True)
            (100 + data2['cumreturns']).plot(ax = axs[3], legend = True)
    if(plotMe):
        for x in plt.get_fignums():
            plt.figure(x)
            plt.show()
    logger.warning('Attempting to save to sql')
    stringPlaceHolder = "".join(stocks)
    #DO NOT CHANGE THIS
    #DO NOT CHANGE THIS FORMATTING
    #DO NOT CHANGE THIS
    d1 = dateFrom.replace('-', "")
    d2 = dateTO.replace('-', "")
    table_name = f"strat_{strat}_view_{view}_lookback_{lookback}_from_{d1}_to_{d2}_stocks_{stringPlaceHolder}"
    table_name = table_name.replace('.', "")
    ans.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.close()
    logger.warning('Attempting to return ans')
    return ans