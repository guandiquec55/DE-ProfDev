'''
This code is for retrieving the data from the API
'''

import requests
import json
import pandas as pd

API_Key = "30c2885d45be728d066c"
URL_Conn_1 = "https://free.currconv.com/api/v7/convert?q="
URL_Conn_2 = "&compact=ultra&apiKey="

def API_Con(a,b):
    x= a + '_' + b
    y= b + '_' + a
    response = requests.get(URL_Conn_1+x+","+y+URL_Conn_2 +API_Key)
    a = response.text

    a_json = json.loads(a)
    df_cur = pd.DataFrame.from_dict(a_json,orient='index')
    
    for k,v in df_cur.items():
        for k1,v1 in v.items():
            return v1