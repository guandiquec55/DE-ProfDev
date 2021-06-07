from db_models import CurrencyRate
from db_utils import insert_sql, read_sql, update_sql
from api_handler import get_latest_rate
import pandas as pd
import datetime
import time

if __name__ == '__main__':
    while True:
        currencies = read_sql(
            "SELECT DISTINCT FromCurrencyCode, ToCurrencyCode FROM [Sales].[CurrencyRate]")
        currencies['CombCurr'] = currencies['FromCurrencyCode'] + \
            '_' + currencies['ToCurrencyCode']
        curr_list_str = list(currencies['CombCurr'].values)
        new_curr_rates = get_latest_rate(curr_list_str)
        dt_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        values = []
        for curr_comb in new_curr_rates.keys():
            from_to = curr_comb.split('_')
            from_code = from_to[0].upper()
            to_code = from_to[1].upper()
            curr_rate = new_curr_rates[curr_comb]
            values.append([dt_time, from_code, to_code, 0, curr_rate, dt_time])
        db_prep = pd.DataFrame(data=values, columns=[
            'CurrencyRateDate', 'FromCurrencyCode', 'ToCurrencyCode', 'AverageRate', 'EndOfDayRate', 'ModifiedDate'])
        insert_sql(CurrencyRate, db_prep.to_dict(orient='records'))
        update_sql("""
                    UPDATE [Sales].[CurrencyRate]
                    SET [Sales].[CurrencyRate].AverageRate = avg.AvgRate
                    FROM (SELECT 
                            FromCurrencyCode,
                            ToCurrencyCode,
                            AVG(EndOfDayRate) as AvgRate 
                            FROM [Sales].[CurrencyRate]
                            GROUP BY FromCurrencyCode, ToCurrencyCode) as avg
                    WHERE avg.FromCurrencyCode = [Sales].[CurrencyRate].FromCurrencyCode
                    AND avg.ToCurrencyCode = [Sales].[CurrencyRate].ToCurrencyCode
                   """)
        time.sleep(3600)  # 1hr
