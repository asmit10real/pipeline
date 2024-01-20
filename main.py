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
d1 = "2019-01-01" #From:
#Must be either same year as FROM OR a few days into new year or else SQL dataExists() WILL fail
d2 = "2024-01-05" #TO:
#15 DOWNTREND 15 UPTREND 20 WHATEVER FOR 2023-01-01 -> 2024-01-05

stocks = [
    "AAPL", "MSFT", "AMZN", "NVDA", "AVGO", 
    "META", "GOOG", "COST", "ADBE", "AMD",
    "NFLX", "INTC", "INTU", "AMAT", "BKNG",
    "NTR", "CTVA", "ADM", "TSN",
    "FSLR", "ENPH", "SEDG", "DQ", "JKS",
    "LUV", "AAL", "UAL", "ALGT", "ALK",
    "VRTX", "GILD", "IQV", "BIIB", "MRNA",
    "ALNY", "SLB", "HAL", "BKR", "TS",
    "NOV", "NE", "RIG", "CHX", "PTEN",
    "PLTR", "PTON", "OII", "RIOT", "TSLA"
]

'''
stocks = [
    "AAPL", "MSFT", "AMZN", "TSLA", "GOOGL", 
    "GOOG", "ZIM", "JNJ", "JPM", "V", 
    "NVDA", "UNH", "META", "PG", "HD", 
    "XOM", "BAC", "MA", "PFE", "DIS", 
    "LLY", "ADBE", "CVX", "COST", "TMO", 
    "PEP", "VZ", "ABBV", "NKE", "CMCSA", 
    "KO", "AVGO", "CSCO", "ACN", "WMT", 
    "MRK", "ABT", "DHR", "NEE", "TXN", 
    "QCOM", "ORCL", "UPS", "LIN", "MCD", 
    "MS", "UNP", "HON", "BMY", "AMD"
]
'''
#stocks = ["AAPL", "AMZN", "ASML", "BHP", "GLEN.L", "GOOG", "META", "MSFT", "NVDA", "QCOM", "RIO", "SHECF", "SUOPY", "TSM"]
#stocks = ["BA", "CHPT", "DIS", "MARA", "NIO", "PFE", "SEDG", "SHOP", "SNOW", "XOM"] #ALPHABETICAL
#stocks = ["RIO", "SPY", "NVDA"]
logger.warning('Attempting to call processDataMultiple(stocks, date1, date2, lookback, view)')
print(f'STRAT: {strat} VIEW: {view} LOOKBACK: {lookback} From: {d1} To: {d2} Stocks: {stocks}')

if(testPerf):
    cProfile.run('results.processDataMultiple(stocks, d1, d2, lookback, view, strat = strat, plotMe = False)', 'profile_stats')
    p = pstats.Stats('profile_stats')
    p.strip_dirs()
    p.sort_stats('time').print_stats(25)
else:
    results.processDataMultiple(stocks, d1, d2, lookback, view, strat = strat, plotMe = False)

#Match formatting to sql formatting
d1 = d1.replace('-', "")
d2 = d2.replace('-', "")
stringName = "".join(stocks).replace(".", "")
tableName = f"strat_{strat}_view_{view}_lookback_{lookback}_from_{d1}_to_{d2}_stocks_{stringName}"
sql.getTables(db="stock_data.db")

bh, strat = results.average(tableName)
print(f"B&Hold Average Profit Factor: {bh[0]} Average PnL: {bh[1]}")
print(f"Strat Average Profit Factor: {strat[0]} Average PnL: {strat[1]}")


#sql.getDataFromTable(tableName, db = "stock_data.db") #output data





#out = x.loc[:, "Profit Factor"].mean()
#out2 = x.loc[:, "PnL"].mean()
#print(out, out2)