import logging
import cProfile
import pstats
import results as results
import sql as sql
logger = logging.getLogger()
logger.setLevel(logging.CRITICAL) #Debug or Critical are used

logger.warning('PROGRAM START')

testPerf = False #Test run time performance?
lookback = 30 #indicator variable
view = 30 #Strategy variable | Changes rolling window size
strat = 3 #Select which strategy you want to use
d1 = "2020-01-01" #From:
d2 = "2024-01-05" #TO: #Must be either same year as FROM OR a few days into new year or else SQL dataExists() WILL fail

#stocks = ["BA", "CHPT", "DIS", "MARA", "NIO", "PFE", "SEDG", "SHOP", "SNOW", "XOM"] #ALPHABETICAL #stocks = ["RIO", "SPY", "NVDA"]
stocks = ["QQQ", "SPY", "RIO"]
if(testPerf):
    cProfile.run('results.processDataMultiple(stocks, d1, d2, lookback, view, strat = strat, plotMe = False)', 'profile_stats')
    p = pstats.Stats('profile_stats')
    p.strip_dirs()
    p.sort_stats('time').print_stats(25)
else:
    results.processDataMultiple(stocks, d1, d2, lookback, view, strat = strat, plotMe = True) # logger.warning('Attempting to call processDataMultiple(stocks, date1, date2, lookback, view)')

#Match formatting to sql formatting
d1 = d1.replace('-', "")
d2 = d2.replace('-', "")
stringName = "".join(stocks).replace(".", "")
tableName = f"strat_{strat}_view_{view}_lookback_{lookback}_from_{d1}_to_{d2}_stocks_{stringName}"
sql.getTables(db="stock_data.db")

bh, strat = results.average(tableName)
print(f"B&Hold Average Profit Factor: {bh[0]} Average PnL: {bh[1]}")
print(f"Strat Average Profit Factor: {strat[0]} Average PnL: {strat[1]}")