import pyodbc
import pandas as pd
import requests
import sqlalchemy
import urllib
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

'''Define run-time variables and connection strings'''

driver ="{FreeTDS}"
server = "127.0.0.1"
port = "1433"
database = "AdventureWorks2019"
db_user = "SA"
db_pswd = "Simple@123"
conn = pyodbc.connect(f"DRIVER={driver};SERVER={server};PORT={port};DATABASE={database};UID={db_user};PWD={db_pswd}", autocommit=True)

db_engine = sqlalchemy.create_engine(f'mssql+pyodbc:///?odbc_connect=' +
    urllib.parse.quote_plus(f'DRIVER={driver};SERVER={server};PORT={port};DATABASE={database};UID={db_user};PWD={db_pswd};TDS_Version=8.0;')
)

base_url = "https://free.currconv.com"
api_key = "384c34d7055e7e97a80d"
exch_rate_endpoint = f"/api/v7/convert"
    
''' Function to load latest currency rates into Sales.CurrencyRate'''
def loadCurrencyRates():
    
    
    currencyPairsDf=pd.read_sql('SELECT distinct FromCurrencyCode, ToCurrencyCode FROM Sales.CurrencyRate', conn)
    
    ### Build query string for API call
    numRows = len(currencyPairsDf)
    pairLimit = 2
    pairList = []
    
    newData = []
    
    for index, row in currencyPairsDf.iterrows():
    
        pairStr = row['FromCurrencyCode']+'_'+row['ToCurrencyCode']
        pairList.append(pairStr)
        
        if len(pairList) == pairLimit or index == numRows - 1:
            payload = ','.join(pairList)
            params = {
                      'q' : payload,
                      'compact' : 'ultra',
                      'apiKey' : {api_key}
                     }
    
            response = requests.Session().get(base_url+exch_rate_endpoint, params = params)
            if response.status_code == 200:
                try:
                    resp = response.json()
                    for key in resp:
                        rowDict = {}
                        FromCurrencyCode = key.split('_')[0]
                        ToCurrencyCode = key.split('_')[1]
                        AverageRate = resp[key]
                        EndOfDayRate = resp[key]
                        
                        rowDict['FromCurrencyCode'] = FromCurrencyCode
                        rowDict['ToCurrencyCode'] = ToCurrencyCode
                        rowDict['AverageRate'] = AverageRate
                        rowDict['EndOfDayRate'] = EndOfDayRate
                        
                        newData.append(rowDict)
                        
                except:
                    print(response.json())
            
            else:
                print(response.json())
                
            
            pairList = []
        
    if len(newData) >  0:
        insertDf = pd.DataFrame(newData)
        insertDf['CurrencyRateDate'] = [datetime.datetime.now() for i in newData]
        insertDf.to_sql("CurrencyRate", schema = 'Sales', con= db_engine, if_exists='append',index=False)
        
    print("Run completed at", str(datetime.datetime.now()))
    
    db_engine.dispose()
    
    return


'''Schedule job to run every hour between the start_date and end_date '''
scheduler = BlockingScheduler()
#scheduler.add_job(loadCurrencyRates, 'interval', seconds=20, start_date='2021-06-04 00:00:00', end_date='2021-06-04 01:45:00')
scheduler.add_job(loadCurrencyRates, 'interval', hours=1, start_date='2021-06-04 00:00:00', end_date='2021-06-06 00:00:00')
scheduler.start()


