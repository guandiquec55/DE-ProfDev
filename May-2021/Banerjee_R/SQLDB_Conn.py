import datetime
import pyodbc
import os
from API_Conn import API_Con
from pandas import DataFrame
from datetime import datetime
'''
This code is to connect to the SQL DB, fetch the currency codes & insert the rates
'''

os.environ["ENDPOINT"]="10.0.0.107,1433"
os.environ["PORT"] = "1433"
os.environ["USERNAME"] = "SA"
os.environ["PASSWORD"] = "P@ssw0rd!0917"
os.environ["DATABASE"] = "AdventureWorks2017"

def SQL_Conn():
    cnxn = pyodbc.connect(
       'DRIVER={ODBC Driver 17 for SQL Server}' + 
       ';SERVER=' + os.environ["ENDPOINT"] + ';UID=' + os.environ["USERNAME"] + ';DATABASE=' + os.environ["DATABASE"] +
       ';PWD=' + os.environ["PASSWORD"]+'; MARS_Connection=Yes')
    cur = cnxn.cursor()
    cur.execute('SELECT DISTINCT [FromCurrencyCode],[ToCurrencyCode] FROM [Sales].[CurrencyRate]')
    a = cur.fetchall()
    results = []
   
    time1 = str(datetime.now())[0:-3]
    for row in a:
        results.append(row)
    
    sql = '''INSERT INTO [AdventureWorks2017].[Sales].[CurrencyRate]
                        (CurrencyRateDate,FromCurrencyCode,ToCurrencyCode,AverageRate,EndOfDayRate,ModifiedDate) 
                        VALUES(?,?,?,?,?,?)'''
    val_fin = []

    df = DataFrame(results)
    for i in range(len(df)):
        a = df.loc[i].to_string().split(',')[0].split('[')[1]
        b = df.loc[i].to_string().split(',')[1].split(']')[0]

        x=API_Con(a.strip(),b.strip())  

        if x is None:
            x=0.0
        
        val = (time1,a.strip(),b.strip(),x,x,time1)
        val_fin.append(val)
    cur.fast_executemany = True
    
    print("No. of items in list:",len(val_fin))
    if len(val)>0:
        cur.executemany(sql,val_fin)
        cnxn.commit()
    else:
        pass

SQL_Conn()
    
