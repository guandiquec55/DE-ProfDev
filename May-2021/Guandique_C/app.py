import pandas as pd
import pyodbc 
import requests
import schedule
import datetime


##Connect to SQL server db
conn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                      "Server=localhost;"
                      "Port=1443;"
                      "UID=CGService;"
                      "PWD=340$Upxap7Mceo7Khy;"
                      'Database=AdventureWorks2019;'
                      'Trusted_Connection=no;'
                      )

cursor = conn.cursor()

##Connect to API - update data in db
def update_currencies(currencies):
    url = 'https://free.currconv.com/api/v7/convert?q=USD_{0}&compact=ultra&apiKey=429a5e1775e66bf985f8'
    if len(currencies) <= 1:
        for each in currencies: 
            r = requests.get(url.format(each))
            update = r.json()
            sql = f'''INSERT INTO [AdventureWorks2019].[Sales].[CurrencyRate] 
                (CurrencyRateDate,FromCurrencyCode,ToCurrencyCode,AverageRate,EndOfDayRate,ModifiedDate)
                VALUES   
                (CURRENT_TIMESTAMP,
                'USD',
                '{each}',
                {update['USD_'+each]},
                {update['USD_'+each]},
                CURRENT_TIMESTAMP);'''
    cursor.execute(query)
    conn.commit()
    else:print("update completed")
    conn.close()


##Trigger application schedule
scheduler = BlockingScheduler()
scheduler.add_job(update_currencies, 'interval', hours=1, start_date='2021-06-01 00:00:00', end_date='2022-06-06 00:00:00')
scheduler.start()
