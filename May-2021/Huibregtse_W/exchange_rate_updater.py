import datetime
from dataclasses import dataclass
import sys, time
from schedule import every, repeat, run_pending
from exchange_rate_api_adapter import ExchangeRateApiAdapter
from db_adapter import DatabaseAdapter
from app_credentials import AppCredentials

@repeat(every(1).hours) #Uncomment to tag this as a scheduled job
def update_rates(credentials : AppCredentials):
    """Main DB Updater Job
    Scheduled runs are handled via the schedule module to run every hour.
    Will skip an hour if it detects the exchange rate api is close to its limit"""
    print('-'*20 + '\n')
    print('Begining Scheduled Exchange Rate Update: {}'.format(datetime.datetime.utcnow().strftime(r'%B %d %Y - %H:%M:%S (UTC)')))

    exchange_rate_adapter = ExchangeRateApiAdapter(credentials.api_key)        
    db_adapter = DatabaseAdapter(credentials)

    unique_rates = db_adapter.get_unique_pairs()
    
    current_usage = exchange_rate_adapter._get_api_usage()
    if current_usage.usage > (100 - len(unique_rates)):
        print('\tWARNING: ExchangeRateAPI hourly usage limit would be exceeded by retrieving this list of rates. Skipping this automatic update...')
        return
    
    print(f'\tINFO: Current Exchange Rate API usage: {current_usage.usage} (100 total / h).')
    
    rate_values = exchange_rate_adapter.get_exchange_rates(unique_rates)
    db_adapter.insert_currency_rates(rate_values)
    print('\tINFO: Exchange rates updated successfully!')
    print('-'*20 + '\n')

if __name__ == "__main__":
    creds = AppCredentials(sys.argv[1], sys.argv[2], sys.argv[3])
    while True:
        run_pending()
        time.sleep(1)