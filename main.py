import logging
import cProfile
import pstats
import results as results
import sql as sql
import json
import indicators.fundamental as fundamental

logger = logging.getLogger()
logger.setLevel(logging.CRITICAL) #Debug or Critical are used

logger.warning('PROGRAM START')

def load_config():
    try:
        with open('config.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("Config file not found. Please ensure config exists.")
        exit(1)
    except json.JSONDecodeError:
        print("Error reading config file.")
        exit(1)

config = load_config()




testPerf = config['variables']['testPerformance'] #Test run time performance?
lookback = config['variables']['lookback'] #indicator variable
view = config['variables']['view'] #Strategy variable | Changes rolling window size
strat = config['variables']['strategy'] #Select which strategy you want to use
d1 = config['variables']['dateFROM'] #From:
d2 = config['variables']['dateTO'] #TO: #Must be either same year as FROM OR a few days into new year or else SQL dataExists() WILL fail

#stocks = ["BA", "CHPT", "DIS", "MARA", "NIO", "PFE", "SEDG", "SHOP", "SNOW", "XOM"] #ALPHABETICAL #stocks = ["RIO", "SPY", "NVDA"]
stocks = ["IBM"]
if(testPerf):
    cProfile.run("results.processDataMultiple(stocks, d1, d2, lookback, view, strat = strat, plotMe = config['variables']['plotMe'])", 'profile_stats')
    p = pstats.Stats('profile_stats')
    p.strip_dirs()
    p.sort_stats('time').print_stats(25)
else:
    results.processDataMultiple(stocks, d1, d2, lookback, view, strat = strat, plotMe = config['variables']['plotMe']) # logger.warning('Attempting to call processDataMultiple(stocks, date1, date2, lookback, view)')

#Match formatting to sql formatting
d1 = d1.replace('-', "")
d2 = d2.replace('-', "")
stringName = "".join(stocks).replace(".", "")
tableName = f"strat_{strat}_view_{view}_lookback_{lookback}_from_{d1}_to_{d2}_stocks_{stringName}"
sql.getTables(db="stock_data.db")

bh, strat = results.average(tableName)
b, c, v = fundamental.getStatements("IBM")
fundamental.createSheet(b, c, v, "IBM")
print(f"B&Hold Average Profit Factor: {bh[0]} Average PnL: {bh[1]}")
print(f"Strat Average Profit Factor: {strat[0]} Average PnL: {strat[1]}")