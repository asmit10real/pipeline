
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

#Probably should use AlphaVantage free plan is 25 calls/day, $25/month = 30 calls per minute

import yfinance as yf
import pandas as pd
import requests
import numpy as np
from pandas import json_normalize
from dotenv import load_dotenv
import os

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

def getStatements(stock: str):
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
    return (balance_sheet, income_statement, cashflow_statement)
# qqq = get("QQQ")
#calc(*qqq)
def calc(balance_sheet: pd.DataFrame, income_statement: pd.DataFrame, cashflow_statement: pd.DataFrame):
    Calculations.shares(balance_sheet)
#print(msft.balance_sheet.iloc[0]) #shares
class Calculations:
    def shares(balance_sheet: pd.DataFrame):
        outstandingshares = balance_sheet.loc[:, 'commonStockSharesOutstanding']
        return outstandingshares
    def revenueTotal(income_statement: pd.DataFrame):
        income = income_statement.loc[:, 'totalRevenue']
        return income
    def revenueTotalAverage3(income_statement: pd.DataFrame):
        revenueAverage = income_statement['totalRevenue'].rolling(window = 3, min_periods = 1).mean()
        return revenueAverage
    #turnover defined not using averages for now need to double check how it's supposed to be calculated
    def turnover(income_statement: pd.DataFrame, balance_sheet: pd.DataFrame):
        turnover = income_statement['totalRevenue'] / balance_sheet['totalAssets']
        return turnover
    def turnoverAverage3(df: pd.DataFrame):
        turnoverAvg = df['turnover'].rolling(window = 3, min_periods=1).mean()
        return turnoverAvg
    def grossIncDivTurnover(income_statement: pd.DataFrame, df: pd.DataFrame):
        grossIncDivTurn = np.where(df['turnover'] > 1, 
                   income_statement['grossProfit'] / df['turnover'], 
                   income_statement['grossProfit'] * df['turnover'])
        return grossIncDivTurn
    def cfEbitDivTurnover(income_statement: pd.DataFrame, cashflow_statement: pd.DataFrame, df: pd.DataFrame):
        ans = (cashflow_statement['operatingCashflow'] + income_statement['incomeTaxExpense'] + income_statement['interestExpense'] + cashflow_statement['depreciationDepletionAndAmortization']) / df['Turnover']
    def roic(income_statement: pd.DataFrame, balance_sheet: pd.DataFrame):
        #nopat
        #nopat = income_statement['operatingIncome'] * (1 - (income_statement['incomeTaxExpense'] / income_statement['incomeBeforeTax']))
        #ic = balance_sheet['totalCurrentAssets'] - balance_sheet['totalCurrentLiabilities'] - balance_sheet['cashAndCashEquivalentsAtCarryingValue'] + balance_sheet['propertyPlantEquipment']
        #roic = nopat / invested capital (ic)
        ans = (income_statement['operatingIncome'] * (1 - (income_statement['incomeTaxExpense'] / income_statement['incomeBeforeTax']))) / (balance_sheet['totalCurrentAssets'] - balance_sheet['totalCurrentLiabilities'] - balance_sheet['cashAndCashEquivalentsAtCarryingValue'] + balance_sheet['propertyPlantEquipment'])
        return ans
    def roicAverage3(df = pd.DataFrame):
        roicAvg3 = df['roic'].rolling(window = 3, min_periods = 1).mean()
        return roicAvg3
    