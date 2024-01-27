
'''
CREATE SQL TABLE OF ALL THIS CRAB FOR database
financial_metrics = [
    "period End", DATE might have to reformat
    "Outstand Sh", bal_sheet[1]
    "Revenues", income_stmt[45]
    "Revs Avg3", average of current and previous two revs (total of 3) minimum window = 1
    "Turnover Avg3", probably should add column for turnover without average but Turnover = $net revenue income_stmt[45] - income_stmt[44]/ $total assets bal_sheet[40] | average of current and previous two turnovers (total of 3) minimum window = 1
    "Gross Inc / TO", If Turnover>1 Gross profit [43] / Turnover if Turnover<1 Gross profit * Turnover
    "cfEBIT adj / TO", CFEBITDA = Cash Flow cash_flow[0]+ Taxes cash_flow[46] + Interest Expense income_stmt[11]+ Depreciation & Amortization cash_flow[49] / Turnover
    "ROIC Avg3", ROIC = NOPAT / Invested Capital | NOPAT=Net operating profit after tax || average of current and previous two ROIC (total of 3) minimum window = 1
    "CROSIC Abg3", #UNKNOWN I really dont remember man
    "Revs /sh", Revenues divided by shares income_stmt[45] / bal_sheet[1]
    "Assets", bal_sheet[40]
    "Assets /sh", Assets divided by shares bal_sheet[40] / bal_sheet[1]
    "Net Excess Cash", Excess Cash = Cash & Equivalents bal_sheet[70] + Long-Term Investments bal_sheet[44] - Current Liabilities bal_sheet[28]
    "Net Common Overhang", Net Common Overhang = LT liabilities bal_sheet[19] + ST debt bal_sheet[32] - Excess Cash & ST Investments bal_sheet[69]
    "Book /sh", Book Value per Share = (total assets bal_sheet[40] - its total liabilities bal_sheet[18]) / Outstanding shares bal_sheet[1]
    "Tang Book /sh", equal to total assets bal_sheet[40] - total liabilities bal_sheet[18] - Intangibles bal_sheet[46]  / Outstanding shares bal_sheet[1]
    "ROE", = Net Profit income_stmt[23] * Turnover * Financial Leverage
    "bm roe", = roe * book to market
    "bm ROE 3yr%", average of current and previous two bm roe (total of 3) minimum window = 1
    "bm ROE 5yr%", average of current and previous 4 bm roe (total of 5) minimum window = 1
    "tbm roe", = roe * tangible book to market
    "tbm ROE 3yr%", average of current and previous two tbm roe (total of 3) minimum window = 1
    "tbm ROE 5yr%", average of current and previous 4 tbm roe (total of 5) minimum window = 1
    "Div /sh", = Dividends paid cash_flow[69] / outstanding shares bal_sheet[1] 
    "bm EPS Avg3yr", #UNKNOWN
    "Ebitda /sh", = EBITDA = Net Income cash_flow[109] + Taxes cash_flow[46]+ Interest Expense income_stmt[11] + Depreciation & Amortization cash_flow[49]) / outstanding shares bal_sheet[1]
    "Ebitda avg3 ;sh", average of current and previous two EBITDA / sh (total of 3) minimum window = 1
    "Ebitda avg7 /sh", average of current and previous 6 EBITDA / sh (total of 7) minimum window = 1

    "Common EPS", = "NetIncomeFromContinuingOperationNetMinorityInterest" income_stmt[5] / outstanding shares bal_sheet[1]

    "Net inc income_stmt[23] avg3 /sh", average of current and previous two Common EPS (total of 3) minimum window = 1
    "Net Inc avg7 /sh", average of current and previous 6 Common EPS (total of 7) minimum window = 1
    "Discount EPS", #UKNOWN iirc he applies a 'discount rate' based somewhat on personal feeling of macro environment or secular movement in that stock's industry
    "CFO /sh", = (Operating Cash Flow = Operating Income cash_flow[53] + Depreciation cash_flow[50] – Taxes cash_flow[46] + Change in Working Capital cash_flow[35]) / outstanding shares bal
        =((VLOOKUP("NetIncomeFromContinuingOperations", $BB$61:$CJ$176, 5, false)) 
        + IFNA((VLOOKUP("Depreciation", $BB$61:$CJ$176, 5, false)), 
        VLOOKUP("DepreciationAndAmortization", $BB$61:$CJ$176, 5, false)) 
        - IFNA(VLOOKUP("DeferredTax", $BB$61:$CJ$158, 5, false), 0) 
        + ((VLOOKUP("CurrentAssets", $A$60:$AD$185, 4, false)
        -VLOOKUP("CurrentLiabilities", $A$60:$AN$167, 4, false))
        -(VLOOKUP("CurrentAssets", $A$60:$AD$185, 5, false)
        -VLOOKUP("CurrentLiabilities", $A$60:$AN$167, 5, false))))
        /Y7



    "CFO Avg3 /sh", average of current and previous two CFO / sh (total of 3) minimum window = 1
    "CFO Avg7 /sh", average of current and previous SIX CFO / sh (total of 7) minimum window = 1
    "SFCF /sh", SFCF = net income income_stmt[23] + depreciation and amortization cash_flow[48] - capital expenditures cash_flow[5] = 
        (VLOOKUP("NetIncomeFromContinuingOperationNetMinorityInterest", $DB$61:$ER$173, 5, false) 
        + VLOOKUP("DepreciationAndAmortization", $BB$61:$CJ$176, 5, false) 
        - VLOOKUP("CapitalExpenditure", $BB$61:$CJ$176, 5, false))/Y7
    "SFCF Avg3 /sh", average of current and previous two SFCF / sh (total of 3) minimum window = 1
    "SFCF abg7 /sh", average of current and previous six SFCF / sh (total of 7) minimum window = 1
    "Net ACGS /sh", UNKNOWN
    "NCF /sh", = Freecashflow cash_flow[0] / sharecount balance_sheet[1] =(VLOOKUP("FreeCashFlow", $BB$61:$CJ$176, 5, false))/Y7
    "NCF avg3 /sh", average of current and previous two NCF / sh (total of 3) minimum window = 1
    "NCF Avg7 /sh", average of current and previous 6 NCF / sh (total of 7) minimum window = 1
    "FIn leverage", Financial Leverage = Average Assets bal_sheet[40] / Average Equity bal_sheet[9] (Common Stock Equity) =((VLOOKUP("TotalAssets", A60:AL155, 4, false) + VLOOKUP("TotalAssets", A60:AL155, 5, false))/2)
        /((VLOOKUP("CommonStockEquity", A60:AL155, 4, false) + VLOOKUP("CommonStockEquity", A60:AL155, 5, false))/2)
    "Net Profit Margin", = Net Income income_stmt[23] / Revenue income_stmt[45]  =VLOOKUP("NetIncome", DB61:EN121, 5, false)/Y8
    "ROIC"
        ROIC = NOPAT / Invested Capital

        NOPAT= Net operating profit after tax = (operating profit) income_stmt[5] x (1 – effective tax rate (bal_sheet[38] / income_stmt[27]))
        ​
        effective tax rate is  divide the income tax expense bal_sheet[38] by the earnings (or income earned) before taxes income_stmt[27].

        invested capital is to obtain the working capital figure by subtracting current liabilities from current assets. (bal_sheet[57] - bal_sheet[28])
        Next, you obtain non-cash working capital by subtracting cash bal_sheet[70] from the working capital value you just calculated. 
        Finally, non-cash working capital is added to a company's fixed assets. (property plant and equipment) bal_sheet[48]

        NOPAT = income_stmt[5] * (1 - (bal_sheet[38] / income_stmt[27]))
        IC = (bal_sheet[57] - bal_sheet[28]) - bal_sheet[70] + bal_sheet[48]
        ROIC = (income_stmt[5] * (1 - (bal_sheet[38] / income_stmt[27]))) / ((bal_sheet[57] - bal_sheet[28]) - bal_sheet[70] + bal_sheet[48])

        =((1 - (VLOOKUP("TaxProvision", $DB$61:$ER$173, 5, false)
        /VLOOKUP("PreTaxIncome", $DB$61:$ER$173, 5, false)))
        *VLOOKUP("NetIncomeFromContinuingOperationNetMinorityInterest", $DB$61:$EQ$178, 5, false))
        /((Y16-VLOOKUP("CurrentLiabilities", $A$60:$AN$167, 4, false))
        -VLOOKUP("CashAndCashEquivalents", $A$60:$AN$167, 4, false) 
        + VLOOKUP("NetPPE", $A$60:$AN$167, 4, false))
    Turnover = Revs / average assets (this year + last /2) = =(AA8/((VLOOKUP("TotalAssets", A60:AL157, 2, false)+VLOOKUP("TotalAssets", A60:AL157, 3,  false))/2))
        income_stmt[45] / bal_sheet[40]
    Book value = Total Assets - TotalLiabilitiesNetMinorityInterest =(AA16-VLOOKUP("TotalLiabilitiesNetMinorityInterest", A60:AL149, 2, FALSE))
        bal_sheet[40] - bal_sheet[18]
    Book to market = =AF7/$AE$6
        Book value / market cap
    Tangible book value = =AF7-VLOOKUP("GoodwillAndOtherIntangibleAssets", A60:AL149, 2, FALSE)
        book value - bal_sheet[45] 
    Tangible book to market = =AH7/$AE$6
        Tangible book value / market cap
    af7 = book value
    ]

'''
'''

msft.income_stmt
msft.balance_sheet
msft.cashflow
'''


import yfinance as yf
import pandas as pd
import requests
import numpy as np
from datetime import datetime, timedelta
from pandas import json_normalize
from dotenv import load_dotenv
import os
import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG) #Debug or Critical are used

logger.debug('start of fundamental.py')

load_dotenv()  # This loads the variables from .env into the environment
apikey = os.environ.get('API_KEY')

'''
# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
# url = f'https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol=IBM&apikey={apikey}'
r = requests.get(url)
dictr = r.json()
reports = dictr['annualReports']

df = json_normalize(reports)
'''

def convert_columns(df: pd.DataFrame):
    columns_to_convert = df.columns.drop('fiscalDateEnding')
    df[columns_to_convert] = df[columns_to_convert].apply(pd.to_numeric, errors='coerce')
    return df


def getStatements(stock: str):
    logger.debug('getting statements')
    #REALLY NEED TO STORE THESE IN SQL
    # Call alphavantage api for balance sheet, cash flow, and income_statement for stock
    url = f'https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={stock}&apikey={apikey}' #Have to change this for each thing
    r = requests.get(url)
    dictr = r.json()
    reports = dictr['annualReports']
    balance_sheet = json_normalize(reports)
    url = f'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={stock}&apikey={apikey}' #Have to change this for each thing
    r = requests.get(url)
    dictr = r.json()
    reports = dictr['annualReports']
    income_statement = json_normalize(reports)
    url = f'https://www.alphavantage.co/query?function=CASH_FLOW&symbol={stock}&apikey={apikey}' #Have to change this for each thing
    r = requests.get(url)
    dictr = r.json()
    reports = dictr['annualReports']
    cashflow_statement = json_normalize(reports)


    # Set each of the csvs to dataframes
    #income_statement = income_statement.to_Frame()
    #cashflow_statement = cashflow_statement.to_Frame()
    logger.debug('returning statements')
    return (balance_sheet, income_statement, cashflow_statement)
# qqq = get("QQQ")
#calc(*qqq)
#Actually creates Roaring Kitty's Spreadsheet
def createSheet(balance_sheet: pd.DataFrame, income_statement: pd.DataFrame, cashflow_statement: pd.DataFrame, tickr: str) -> pd.DataFrame:

    # Extract the 'fiscalDateEnding' columns from each DataFrame
    dates_balance_sheet = set(balance_sheet['fiscalDateEnding'])
    dates_income_statement = set(income_statement['fiscalDateEnding'])
    dates_cash_flow_statement = set(cashflow_statement['fiscalDateEnding'])
    # Add more dates sets as needed

    # Find the intersection (common dates) across all DataFrames
    common_dates = dates_balance_sheet.intersection(dates_income_statement, dates_cash_flow_statement)
    # Add more sets as needed

    # Filter each DataFrame to include only rows with common dates
    balance_sheet = balance_sheet[balance_sheet['fiscalDateEnding'].isin(common_dates)]
    income_statement = income_statement[income_statement['fiscalDateEnding'].isin(common_dates)]
    cashflow_statement = cashflow_statement[cashflow_statement['fiscalDateEnding'].isin(common_dates)]
    # Apply this filtering to all relevant DataFrames

    # Now proceed with your data processing on these filtered DataFrames

    years = []

    for year in income_statement['fiscalDateEnding']:
        years.append(datetime.strptime(year, '%Y-%m-%d'))
    




    balance_sheet = balance_sheet.sort_index(ascending=True)
    logger.debug(balance_sheet)
    income_statement = income_statement.sort_index(ascending=True)
    cashflow_statement = cashflow_statement.sort_index(ascending=True)
    balance_sheet = convert_columns(balance_sheet)
    income_statement = convert_columns(income_statement)
    cashflow_statement = convert_columns(cashflow_statement)

    years = []
    metrics = ['PeriodEnd', 'OutstandingShares', 'Revenues']

    
    for year in income_statement['fiscalDateEnding']:
        years.append(year)
    
    print(years)

    print(cashflow_statement)

    #Verify all the dates line up
    logger.debug('Verifying dates of financial statements align')
    if(balance_sheet.iloc[0]['fiscalDateEnding'] != income_statement.iloc[0]['fiscalDateEnding'] or cashflow_statement.iloc[0]['fiscalDateEnding'] != income_statement.iloc[0]['fiscalDateEnding']):
        return "FUNDAMENTAL DATA DATES DO NOT ALIGN"
    
    resultDf = pd.DataFrame(index = metrics, columns = years)
    print(resultDf)

    calculationsDf = pd.DataFrame()
    

    marketValuesDf = Calculations.marketValueForAllDates(balance_sheet, tickr)
    # print(marketValuesDf)
    logger.debug('Created calculations, result, and marketValue frames')
    # Need to substantially rework some of these functions. Wont work as written
    # Basically any function that works with a mix of the financial statements and the result dataframe at the same time needs to be looked at
    debug = income_statement['fiscalDateEnding']
    labelList = income_statement['fiscalDateEnding'].tolist()

    resultDf.loc['PeriodEnd'] = labelList
    shares_series = Calculations.shares(balance_sheet)
    shares_series.index = resultDf.columns  # Aligning the Series index with DataFrame columns
    resultDf.loc['OutstandingShares'] = shares_series
    #resultDf.loc['OutstandingShares'] = Calculations.shares(balance_sheet)
    result_series = Calculations.revenueTotal(income_statement)
    result_series.index = resultDf.columns
    resultDf.loc['Revenues'] = result_series
    #resultDf.loc['Revenues'] = Calculations.revenueTotal(income_statement).T
    resultDf.loc['RevenueAverage3'] = Calculations.revenueTotalAverage3(income_statement).T
    turnover_series = Calculations.turnover(income_statement, balance_sheet)
    turnover_series.index = resultDf.columns
    resultDf.loc['Turnover'] = turnover_series
    #resultDf.loc['Turnover'] = Calculations.turnover(income_statement, balance_sheet).T
    resultDf.loc['TurnoverAverage3'] = Calculations.turnoverAverage3(resultDf)
    grincturn_series = Calculations.grossIncDivTurnover(income_statement, resultDf)
    grincturn_series.index = resultDf.columns
    resultDf.loc['Gross Income / Turnover'] = grincturn_series
    fin_series = Calculations.financialLeverage(balance_sheet)
    fin_series.index = resultDf.columns
    resultDf.loc['Financial Leverage'] = fin_series
    cf_series = Calculations.cfEbitDivTurnover(income_statement, cashflow_statement, resultDf)
    cf_series.index = resultDf.columns
    resultDf.loc['Cashflow EBITDA / Turnover'] = cf_series
    roic_series = Calculations.roic(income_statement, balance_sheet)
    roic_series.index = resultDf.columns
    resultDf.loc['Return On Investment Capital'] = roic_series
    resultDf.loc['roicAverage3'] = Calculations.roicAverage3(resultDf)
    revPshare_series = Calculations.revsPerShare(income_statement, balance_sheet)
    revPshare_series.index = resultDf.columns
    resultDf.loc['RevenuePerShare'] = revPshare_series
    assets_series = Calculations.assets(balance_sheet)
    assets_series.index = resultDf.columns
    resultDf.loc['Total Assets'] = assets_series
    assetsPshare_series = Calculations.assetsPerShare(resultDf)
    assetsPshare_series.index = resultDf.columns
    resultDf.loc['Assets Per Shares'] = assetsPshare_series
    excessCash_series = Calculations.excessCash(balance_sheet)
    excessCash_series.index = resultDf.columns
    resultDf.loc['Excess Cash'] = excessCash_series
    neo_series = Calculations.netCommonOverhang(balance_sheet, resultDf)
    neo_series.index = resultDf.columns
    resultDf.loc['Net Common Overhang'] = neo_series
    bvps_series = Calculations.bookValuePerShare(balance_sheet)
    bvps_series.index = resultDf.columns
    resultDf.loc['Book Value Per Share'] = bvps_series
    tbvps_series = Calculations.tangibleBookValuePerShare(balance_sheet)
    tbvps_series.index = resultDf.columns
    resultDf.loc['Tangible Book Value Per Share'] = tbvps_series
    roe_series = Calculations.returnOnEquity(income_statement, resultDf)
    roe_series.index = resultDf.columns
    resultDf.loc['Return On Equity'] = roe_series
    bvalue_series = Calculations.bookValue(balance_sheet)
    bvalue_series.index = resultDf.columns
    resultDf.loc['Book Value'] = bvalue_series
    tbvalue_series = Calculations.tangibleBookValue(balance_sheet, resultDf)
    tbvalue_series.index = resultDf.columns
    resultDf.loc['Tangible Book Value'] = tbvalue_series
    btm_series = Calculations.bookToMarket(marketValuesDf, resultDf)
    btm_series.index = resultDf.columns
    resultDf.loc['Book To Market'] = btm_series #I really need to check if i need to transpose funcs like this its kinda confusing tbh
    resultDf.loc['BooktoMarketReturnOnEquity'] = Calculations.bookToReturnOnEquity(resultDf)
    resultDf.loc['BtM Return On Equity 3yr'] = resultDf.loc['BooktoMarketReturnOnEquity'].rolling(window = 3, min_periods = 1).mean()
    resultDf.loc['BtM Return On Equity 5yr'] = resultDf.loc['BooktoMarketReturnOnEquity'].rolling(window = 5, min_periods = 1).mean()
    tbm_series = Calculations.tangibleBookToMarket(marketValuesDf, resultDf)
    tbm_series.index = resultDf.columns
    resultDf.loc['Tangible Book To Market'] = tbm_series
    tbmroe_series = Calculations.tangibleBookToReturnOnEquity(resultDf)
    tbmroe_series.index = resultDf.columns
    resultDf.loc['TangibleBooktoMarketReturnOnEquity'] = tbmroe_series
    resultDf.loc['Tangible BtM Return on Equity 3yr'] = resultDf.loc['TangibleBooktoMarketReturnOnEquity'].rolling(window = 3, min_periods = 1).mean()
    resultDf.loc['Tangible BtM Return on Equity 5yr'] = resultDf.loc['TangibleBooktoMarketReturnOnEquity'].rolling(window = 5, min_periods = 1).mean()
    divPerShare_series = Calculations.dividendsPerShare(cashflow_statement, balance_sheet)
    divPerShare_series.index = resultDf.columns
    resultDf.loc['Dividend Paid Per Share'] = divPerShare_series
    ebitdaPerShare_series = Calculations.ebitdaPerShare(cashflow_statement, balance_sheet, income_statement)
    ebitdaPerShare_series.index = resultDf.columns
    resultDf.loc['EBITDA Per Share'] = ebitdaPerShare_series
    resultDf.loc['EBITDA Average 3yr'] = Calculations.ebitdaPerShareAverage3(resultDf)
    resultDf.loc['EBITDA Average 7yr'] = Calculations.ebitdaPerShareAverage7(resultDf)
    niPerShare_series = Calculations.commonEarningsPerShare(income_statement, balance_sheet)
    niPerShare_series.index = resultDf.columns
    resultDf.loc['Net Income Per Share'] = niPerShare_series
    resultDf.loc['Net Income Per Share Average 3'] = Calculations.commonEarningsPerShareAverage3(resultDf)
    resultDf.loc["Net Income Per Share Average 7"] = Calculations.commonEarningsPerShareAverage7(resultDf)
    sfcPerShare_series = Calculations.simpleFreeCashFlowPerShare(income_statement, cashflow_statement, balance_sheet)
    sfcPerShare_series.index = resultDf.columns
    resultDf.loc['Simple Free Cashflow Per Share'] = sfcPerShare_series
    resultDf.loc['Simple Free Cashflow Per Share Average 3'] = Calculations.simpleFreeCashFlowPerShareAverage3(resultDf)
    resultDf.loc['Simple Free Cashflow Per Share Average 7'] = Calculations.simpleFreeCashFlowPerShareAverage7(resultDf)
    ncfPerShare_series = Calculations.netCashFlowPerShare(cashflow_statement, balance_sheet)
    ncfPerShare_series.index = resultDf.columns
    resultDf.loc['Net Cashflow Per Share'] = ncfPerShare_series
    resultDf.loc['Net Cashflow Per Share Average 3'] = Calculations.netCashFlowPerShareAverage3(resultDf)
    resultDf.loc['Net Cashflow Per Share Average 7'] = Calculations.netCashFlowPerShareAverage7(resultDf)
    npm_series = Calculations.netProfitMargin(income_statement)
    npm_series.index = resultDf.columns
    resultDf.loc['Net Profit Margin'] = npm_series
    print(resultDf)
    #print(resultDf.describe())
    #print(resultDf.shape)
    #Calculations.shares(balance_sheet)

class Calculations:
    def shares(balance_sheet: pd.DataFrame):
        outstandingshares = balance_sheet['commonStockSharesOutstanding']
        print(outstandingshares)
        return outstandingshares
    def revenueTotal(income_statement: pd.DataFrame):
        income = income_statement['totalRevenue']
        return income
    def revenueTotalAverage3(income_statement: pd.DataFrame):
        revenueAverage = income_statement['totalRevenue'].rolling(window = 3, min_periods = 1).mean()
        return revenueAverage
    #turnover defined not using averages for now need to double check how it's supposed to be calculated
    def turnover(income_statement: pd.DataFrame, balance_sheet: pd.DataFrame):
        income_statement = income_statement.reset_index(drop=True)
        balance_sheet = balance_sheet.reset_index(drop=True)
        turnover = income_statement['totalRevenue'] / balance_sheet['totalAssets']
        return turnover
    def turnoverAverage3(df: pd.DataFrame):
        turnoverAvg = df.loc['Turnover'].rolling(window = 3, min_periods=1).mean()
        return turnoverAvg
    def grossIncDivTurnover(income_statement: pd.DataFrame, df: pd.DataFrame):
        # Assuming 'grossProfit' is from 'income_statement' and matches the years in 'df'
        gross_profit = income_statement['grossProfit']
        turnover = df.loc['Turnover']
        gross_profit = gross_profit.reset_index(drop = True)
        turnover = turnover.reset_index(drop = True)

        grossIncDivTurn = np.where(turnover > 1, 
                   gross_profit / turnover, 
                   gross_profit * turnover)
        
        grossIncDivTurn = pd.Series(grossIncDivTurn, index=df.columns)


        return grossIncDivTurn
    def cfEbitDivTurnover(income_statement: pd.DataFrame, cashflow_statement: pd.DataFrame, df: pd.DataFrame):
        operating_cash_flow = cashflow_statement['operatingCashflow']
        operating_cash_flow = operating_cash_flow.reset_index(drop = True)
        incomeTaxExpense = income_statement['incomeTaxExpense']
        incomeTaxExpense = incomeTaxExpense.reset_index(drop = True)
        interestExpense = income_statement['interestExpense']
        interestExpense = interestExpense.reset_index(drop = True)

        depreciationExpense = cashflow_statement['depreciationDepletionAndAmortization']
        depreciationExpense = depreciationExpense.reset_index(drop = True)

        turnover = df.loc['Turnover']
        turnover = turnover.reset_index(drop = True)
    
        income_statement = income_statement.reset_index(drop=True)
        cashflow_statement = cashflow_statement.reset_index(drop=True)
        res = (operating_cash_flow + incomeTaxExpense + interestExpense + depreciationExpense) / turnover
        return res
    def roic(income_statement: pd.DataFrame, balance_sheet: pd.DataFrame):
        #nopat
        #nopat = income_statement['operatingIncome'] * (1 - (income_statement['incomeTaxExpense'] / income_statement['incomeBeforeTax']))
        #ic = balance_sheet['totalCurrentAssets'] - balance_sheet['totalCurrentLiabilities'] - balance_sheet['cashAndCashEquivalentsAtCarryingValue'] + balance_sheet['propertyPlantEquipment']
        #roic = nopat / invested capital (ic)
        return (income_statement['operatingIncome'] * (1 - (income_statement['incomeTaxExpense'] / income_statement['incomeBeforeTax']))) / (balance_sheet['totalCurrentAssets'] - balance_sheet['totalCurrentLiabilities'] - balance_sheet['cashAndCashEquivalentsAtCarryingValue'] + balance_sheet['propertyPlantEquipment'])
    def roicAverage3(df: pd.DataFrame):
        roicAvg3 = df.loc['Return On Investment Capital'].rolling(window = 3, min_periods = 1).mean()
        return roicAvg3
    def revsPerShare(income_statement: pd.DataFrame, balance_sheet: pd.DataFrame):
        revsPShare = income_statement['totalRevenue'] / balance_sheet['commonStockSharesOutstanding']
        return revsPShare
    def assets(balance_sheet: pd.DataFrame):
        return balance_sheet['totalAssets']
    def assetsPerShare(df: pd.DataFrame):
        return df.loc['Total Assets'] / df.loc['OutstandingShares']
    def excessCash(balance_sheet: pd.DataFrame):
        return balance_sheet['cashAndCashEquivalentsAtCarryingValue'] + balance_sheet['longTermInvestments'] - balance_sheet['totalCurrentLiabilities']
    def netCommonOverhang(balance_sheet: pd.DataFrame, df: pd.DataFrame):
        balance_sheet = balance_sheet.reset_index(drop = True)
        z = df.loc['Excess Cash']
        z = z.reset_index(drop = True)
        return balance_sheet['totalNonCurrentLiabilities'] + balance_sheet['shortTermDebt'] - balance_sheet['shortTermInvestments'] - z
    def bookValuePerShare(balance_sheet: pd.DataFrame):
        return (balance_sheet['totalAssets'] - balance_sheet['totalLiabilities']) / balance_sheet['commonStockSharesOutstanding']
    def tangibleBookValuePerShare(balance_sheet: pd.DataFrame):
        return (balance_sheet['totalAssets'] - balance_sheet['totalLiabilities'] - balance_sheet['intangibleAssets']) / balance_sheet['commonStockSharesOutstanding']
    #Naive implementation of financial leverage, Roaring Kitty uses an average of this years and previous years iirc
    def financialLeverage(balance_sheet: pd.DataFrame):
        return balance_sheet['totalAssets'] / balance_sheet['totalShareholderEquity']
    def returnOnEquity(income_statement: pd.DataFrame, df: pd.DataFrame):
        x = df.loc['Turnover']
        y = df.loc['Financial Leverage']
        z = income_statement['netIncome']
        x = x.reset_index(drop = True)
        y = y.reset_index(drop = True)
        z = z.reset_index(drop = True)
        return z * x * y
    def bookToMarket(marketValues: pd.DataFrame, resultFrame: pd.DataFrame):
        return resultFrame.loc['Book Value'] / marketValues['marketVal']
    def tangibleBookToMarket(marketValues: pd.DataFrame, resultFrame: pd.DataFrame):
        x = resultFrame.loc['Tangible Book Value']
        y = marketValues['marketVal']
        x = x.reset_index(drop = True)
        y = y.reset_index(drop = True)
        return x / y
    def bookToReturnOnEquity(resultFrame: pd.DataFrame):
        return resultFrame.loc['Book To Market'] * resultFrame.loc['Return On Equity']
    def tangibleBookToReturnOnEquity(resultFrame: pd.DataFrame):
        return resultFrame.loc['Tangible Book To Market'] * resultFrame.loc['Return On Equity']
    #Need to implement querying data from sql or yf (if not in sql) to get historic market value of stock for different reporting periods
    def dividendsPerShare(cashflow_statement: pd.DataFrame, balance_sheet: pd.DataFrame):
        return cashflow_statement['dividendPayout'] / balance_sheet['commonStockSharesOutstanding']
    def ebitdaPerShare(cashflow_statement: pd.DataFrame, balance_sheet: pd.DataFrame, income_statement: pd.DataFrame):
        return (income_statement['netIncome'] + income_statement['incomeTaxExpense'] + income_statement['interestExpense'] + income_statement['depreciationAndAmortization']) / balance_sheet['commonStockSharesOutstanding']
    def ebitdaPerShareAverage3(df: pd.DataFrame):
        return df.loc['EBITDA Per Share'].rolling(window = 3, min_periods= 1).mean()
    def ebitdaPerShareAverage7(df: pd.DataFrame):
        return df.loc['EBITDA Per Share'].rolling(window = 7, min_periods = 1).mean()
    #Should be subtrating minority interest from netIncomeFromCont..., haven't implemented it
    def commonEarningsPerShare(income_statement: pd.DataFrame, balance_sheet: pd.DataFrame):
        return income_statement['netIncomeFromContinuingOperations'] / balance_sheet['commonStockSharesOutstanding']
    def commonEarningsPerShareAverage3(df: pd.DataFrame):
        return df.loc['Net Income Per Share'].rolling(window = 3, min_periods = 1).mean()
    def commonEarningsPerShareAverage7(df: pd.DataFrame):
        return df.loc['Net Income Per Share'].rolling(window = 7, min_periods = 1).mean()
    def simpleFreeCashFlowPerShare(income_statement: pd.DataFrame, cashflow_statement: pd.DataFrame, balance_sheet: pd.DataFrame):
        return (cashflow_statement['netIncome'] + income_statement['depreciationAndAmortization'] - cashflow_statement['capitalExpenditures']) / balance_sheet['commonStockSharesOutstanding']
    def simpleFreeCashFlowPerShareAverage3(df: pd.DataFrame):
        return df.loc['Simple Free Cashflow Per Share'].rolling(window = 3, min_periods = 1).mean()
    def simpleFreeCashFlowPerShareAverage7(df: pd.DataFrame):
        return df.loc['Simple Free Cashflow Per Share'].rolling(window = 7, min_periods = 1).mean()
    def netCashFlowPerShare(cashflow_statement: pd.DataFrame, balance_sheet: pd.DataFrame):
        return cashflow_statement['operatingCashflow'] / balance_sheet['commonStockSharesOutstanding']
    def netCashFlowPerShareAverage3(df: pd.DataFrame):
        return df.loc['Net Cashflow Per Share'].rolling(window = 3, min_periods = 1).mean()
    def netCashFlowPerShareAverage7(df: pd.DataFrame):
        return df.loc['Net Cashflow Per Share'].rolling(window = 7, min_periods = 1).mean()
    def netProfitMargin(income_statement: pd.DataFrame):
        return income_statement['netIncome'] / income_statement['totalRevenue']
    def bookValue(balance_sheet: pd.DataFrame):
        return (balance_sheet['totalAssets'] - balance_sheet['totalLiabilities'])
    def tangibleBookValue(balance_sheet: pd.DataFrame, df: pd.DataFrame):
        x = df.loc['Book Value']
        y = balance_sheet['intangibleAssets']
        x = x.reset_index(drop = True)
        y = y.reset_index(drop = True)
        return x - y
    def marketValueForSpecificFilingDate(balance_sheet: pd.DataFrame, ticker: str, filing_date: str):
        balance_sheet = balance_sheet.copy()
        balance_sheet.set_index("fiscalDateEnding", inplace = True)
        #idk if any of this is necessarily the best implementation or necessary but let's work from it
        #convert string t odatetime
        filing_date_date = datetime.strptime(filing_date, "%Y-%m-%d")
        #create date range to get average incase of day of filing date not existing
        start_date = filing_date_date - timedelta(days = 2)
        end_date = filing_date_date + timedelta(days = 2)
        #NEED TO REMEMBER TO SET fiscalDateEnding AS INDEX FOR THIS TO WORK AND ALSO ITS A GOOD THING TO DO IN GENERAL
        #WARNING WARNING WARNING
        stock_data = yf.download(ticker, start=start_date, end=end_date, interval="1d")
        average_close = stock_data['Close'].mean() 
        marketVal = average_close * int(balance_sheet.loc[filing_date, 'commonStockSharesOutstanding'])
        return marketVal
    def marketValueForAllDates(balance_sheet: pd.DataFrame, ticker: str) -> pd.DataFrame:
        market_values = pd.DataFrame(columns=['marketVal'])

        for filing_date in balance_sheet['fiscalDateEnding']:
            #Calculate market value for each filing date
            market_val = Calculations.marketValueForSpecificFilingDate(balance_sheet, ticker, filing_date)

            #Append results
            market_values.loc[filing_date] = market_val
        return market_values



    #need to implement book to market and tangible book to market, but that requires implementing getting a rough est of the market price of the
    #stock at the time

#print(type(x))
#createSheet(b, c, v)
#Syntax for getting the last fin statement where b is the type of fin statement
#print(b.iloc[-1])
