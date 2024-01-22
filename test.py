import requests
from pandas import json_normalize
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()  # This loads the variables from .env into the environment
apikey = os.environ.get('API_KEY')

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = f'https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol=IBM&apikey={apikey}'
r = requests.get(url)
dictr = r.json()
reports = dictr['annualReports']

df = json_normalize(reports)

print(df)
'''
recs = dictr['result']['records']
df = json_normalize(recs)
print(df)

'''


