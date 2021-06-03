import pyodbc
from datetime import date, datetime
from app_credentials import AppCredentials
from typing import Dict

class DatabaseAdapter():
    def __init__(self, app_credentials : AppCredentials):
        self.db_user = app_credentials.db_user
        self.db_pass = app_credentials.db_pass
        self.db_host = app_credentials.db_host
        self.con_str = 'Driver={ODBC Driver 17 for SQL Server};SERVER='+self.db_host+';DATABASE=AdventureWorks2019;UID='+self.db_user+';PWD='+self.db_pass+';'

    def _connect(self):
        """
        Returns a connection to the adventureworks db
        """
        return pyodbc.connect(self.con_str)

    def get_unique_pairs(self):
        """
        Pulls unique currency pairs
        """
        with self._connect() as cnxn:
            cursor = cnxn.cursor()
            sql = 'SELECT DISTINCT cr.FromCurrencyCode, cr.ToCurrencyCode \
                FROM Sales.CurrencyRate cr'
            cursor.execute(sql)
            results = cursor.fetchall()
        return results

    def insert_currency_rates(self, rates_dictionary : dict):
        """
        Loads rates from dictionary
        """
        timestamp = datetime.utcnow()
        sql = 'INSERT INTO Sales.CurrencyRate(CurrencyRateDate, FromCurrencyCode, ToCurrencyCode, AverageRate, EndOfDayRate)\
            VALUES (?,?,?,?,?)'
        rate_dict_as_list = [(timestamp,curr_from,curr_to,rates_dictionary[(curr_from, curr_to)],rates_dictionary[(curr_from, curr_to)]) for curr_from,curr_to in rates_dictionary]
        with self._connect() as cnxn:
            cursor = cnxn.cursor()
            cursor.executemany(sql, rate_dict_as_list)