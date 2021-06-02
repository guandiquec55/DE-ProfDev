# -*- coding: utf-8 -*-
import json
import requests 
import pyodbc
import schedule
import time

def update_rates(currencies):
    """Requests latest conversion rate and inserts into MSSQL instance

    Parameters
    -------
    currencies : list
        List of currencies in CurrencyRate that are available in API

    Returns
    -------
    None.

    """
    
    url = 'https://free.currconv.com/api/v7/convert?q=USD_{0}&compact=ultra&apiKey=d0171c582064aef4f066'
    
    if len(currencies) > 1:
        for each in currencies:
        
            r = requests.get(url.format(each))
            update = r.json()
            try:
                if update['status'] == 400:
                    print('API limit reached, wait 1 hour and try again')
                    return
            except KeyError:
                
                sql = f'''INSERT INTO [AdventureWorks2019].[Sales].[CurrencyRate] 
                (CurrencyRateDate,FromCurrencyCode,ToCurrencyCode,AverageRate,EndOfDayRate,ModifiedDate)
                VALUES   
                (CURRENT_TIMESTAMP,
                'USD',
                '{each}',
                {update['USD_'+each]},
                {update['USD_'+each]},
                CURRENT_TIMESTAMP);'''
                query(sql,'update')
            #print(sql)
    else:
        print('No currencies have been updated')
        
def query(sql,mode):
    """Executes a query via pyodbc connection
    
    Parameters
    -------
    sql : string
        SQL query that is executed on the MSSQL instance
    mode : string
        string to determine functionality of query
    
    Returns
    -------
    results : list or nothing, depending on mode
        Results of query based on mode selected
    
    """
    
    try:
        conn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                          "Server=localhost;"
                          "UID=sa;"
                          "PWD=?A!.k?i6.0g?8?h?;"
                          "Port=1443;"
                          "Database=AdventureWorks2019;"
                          "Trusted_Connection=no;")
        cursor = conn.cursor()
        cursor.execute(sql)

        if mode == 'select':
            results=cursor.fetchall()
            cursor.close()
            conn.close()
            return results
        if mode == 'update':
            conn.commit()
            cursor.close()
            conn.close()
            return

    except:
        cursor.close()
        conn.close()
        print('Unable to connect and query the database')

def get_keys():
    """
    Returns a list of currencies that are in the database and conversion rate is available in the API
    
    Returns
    -------
    currencies : a list of valid keys for the API
    """
    
    r = requests.get('https://free.currconv.com/api/v7/currencies?apiKey=d0171c582064aef4f066')
    try:
        valid_keys = r.json()['results']
    except KeyError:
            print('You have reached the free API limit, wait 1 hour and try again')
            return []
    #currencies = query mssql to pull distinct ToCurrencyCode
    #currencies = ['DEM','CAD','BRL','USD','FRF','CNY','GBP','VEB','SAR','AUD','ARS','EUR','MXN','JPY']
    sql = 'select distinct [ToCurrencyCode] FROM [AdventureWorks2019].[Sales].[CurrencyRate];'
    results = query(sql,'select')
    currencies = []
    for each in results:
        if each[0] in valid_keys:
            currencies.append(each[0])
        else:
            print('Conversion rate not available for:',each[0])
    
    return currencies

def job():
    """
    Calls gets_keys(), stores the list, then calls update_rates on that list
    Returns
    -------
    None.
    """
    currencies = get_keys()
    update_rates(currencies)
    
    

####main
#SA_PASSWORD='?A!.k?i6.0g?8?h?'
#schedule.get_jobs()
#schedule.clear()
schedule.every().hour.at(":01").do(job)

while 1:
    schedule.run_pending()
    time.sleep(1)
#test = '''SELECT TOP (20) [CurrencyRateID]
#       ,[CurrencyRateDate]
#       ,[FromCurrencyCode]
#       ,[ToCurrencyCode]
#       ,[AverageRate]
#       ,[EndOfDayRate]
#       ,[ModifiedDate]
#   FROM [AdventureWorks2019].[Sales].[CurrencyRate] order by CurrencyRateID desc;'''
#test_results = query(test,'select')
