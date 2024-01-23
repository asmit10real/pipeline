**GOAL**: The goal of this program is to allow for quick multivariate analysis for a wide range of stock trading hypotheses.

## fundamental.py
  - Used for all handling of fundamental data and calculations related to it. This is where all the Roaring Kitty analysis happens
  - Very much a WIP
  - getStatements() takes a stock ticker and gets cashflow_statement, balance_sheet, and income_statement. returns them as individual dataframes
  - calc() will be renamed, this will be the function that 'builds' the dataframe(spreadsheet) using all the other functions
  - class Calculations contains all the calculations I had in my attempt to recreate roaring kitty's spreadsheet. If you're aware of his work and notice a calculation missing please add it.

## indicators.py
  - VWAP() calculates vwap
  - AVWAP() takes var window_days calculates vwap with a rolling window average
  - rest of functions are various functions used to generate a trendline indicator. Probably very messy and almost certainly needs refactor

## main.py
  - testPerf = False // True runs performance calculations on the code
  - lookback // should be refactored as its a var for an indicator
  - view // should be refactored as its a var for a strategy
  - strat // int representing the strategy you're picking. Need to think of better solution
  - d1 // string of date that you start at year-month-day
  - d2 // end date string year-month-day
  - stocks = [] // list of stock tickers you want to analyze
  - if(testPerf) ignore this if you set it to false, but if True you need to change the function call to processDataMultiple in this aswell
   ### MAIN FUNCTION CALL
  - results.processDataMultiple(stocks, d1, d2, lookback, view, strat = strat, plotMe = True) this is the MEAT of the program. Analyzes all the stocks you have in your list
  - and calls all other functions. Plots and or outputs results for strategy and stocks you selected.
Below that is formatting for sql and for convenience of messing with random tests.

## performance.py
  Used for calculating various performance metrics
  - calc() calculates various metrics..
  - output() writes certain metrics to console
  - basePerf() returns profit factor, sharpe and sortino ratios for stock.

## raw_data.db
  Database for storing RAW ohlc and volume data from yfinance

## results.py
  Main code for handling the processing of the data and the performance results
  - processData() used for calculating various performance metrics for the stock
  - average() should probably be in sql.py idk messy code for getting the average of the buy and hold & strategy performance results. Used when manually messing with things not sure if this is called anywhere
  - processDataMultiple() This is lazily done for now as it takes some input args related to strategies, when they should be seperate. That being said this func takes a list of stocks, date from, date to, an indicator variable "lookback" and a strategy variable "view" (these are the things that need to be refactored) along with an int representing the strategy being selected, and plotMe which is a bool that decides whether or not to plot performance plots for the list of stocks.
  - There's also initial_balance and position_size_percent again this was hastily done but this is for generating the equity curve, should probably be a var that you can change in main

## signals.py
  - Used to generate buy or sell signals based on strategy selected. Most of the functions need to be moved to indicators.py
  - signal() this is a really messy function right now but it's currently setup to handle the strategy logic for each strategy. I want to make this more clear as I want to be able to mix and match indicators as well as strategy logic.
  - a dumb example is lets say RSI strat that uses signal generated from RSI is returning a 1, and you want to combine that with a VWAP strategy to only have the final signal return 1 when they both return 1
  - This should be possible and modular just like combining indicators to generate a strategy will be

## sql.py
  - Contains all sql functionality
    - deleteTable() deletes table in db
    - getTables() lists all the tables in the db
    - writeRaw() writes the raw data to the raw_data db
    - exists() checks to see if data for a specific stock & time period exists in the DB to avoid downloading from yfinance again
    - getData() used to get the data from sql
    - 
## stock_data.db
  Database for storing log data and ideally any calculations made on the raw data that may be reused later (again from yfinance)

## temp.csv
  - temp file used for thoughts & notes that have no real place in code / too bulky
