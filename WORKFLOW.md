## Setup
1. **Fundamental Analysis**: In order for the fundamental analysis portion of the code to work you have to get an api key from Alphavantage. Free rate-limited keys are available. Create a file called ".env" (with no name) and write API_KEY="your_key_inside_these_quotes" Currently the code will crash if you dont have a key
2. **Configure settings in json**: 
3. **Define list of stocks in main.py** It's best practice to keep the list in alphabetical order. Can easily be done with chatgpt or similar. Useful for not copying database tables unnecessarily

## Program Workflow
1. **Initialization**: program loads key variables from config.json. Loads list of stocks to test performance on from 'stocks = []'
2. **Data Importing**: Attempts to get ohlc and fundamental data from a sqlite db. If not found, will get ohlc data from yfinance and fundamental data from AlphaVantage. Stores raw ohlc data in db along with (some) results from the test. Need to implement saving fundamental data to db.
3. **Strategy Signal Generated**: Signal of 1, 0, or -1 is generated based on logic referencing indicators defined in the indicators subdir.
4. **Performance Analysis**: Performance of the strategy is computed using those signals and compared against buy and hold returns over the same time period.
5. **Results Shown**: If plotMe = True, plots are shown for each of the stocks tested alongside certain performance metrics being printed out. If false, just the metrics are outputted.




