import requests, json
from dataclasses import dataclass
from typing import Dict, Tuple
from datetime import datetime
  
@dataclass
class ExchangeRate():
    """Dataclass to track exchange rate api data for a specific currency pair"""
    id : str
    val : float
    to : str
    fr : str

@dataclass
class ExchangeRateResponse():
    """Dataclass to track data returns by successful api call"""
    query : Dict[str,int]
    results : Dict[str,ExchangeRate]

@dataclass
class ExchangeRateUsageResponse():
    """Dataclass to capture data returned by currency converter usage endpoint"""
    timestamp: str
    usage: int

class ExchangeRateApiAdapter():
    url_base = 'https://free.currconv.com'
    convert_endpoint = '/api/v7/convert'
    usage_endpoint = '/others/usage'

    def __init__(self, api_key):
        self.api_key = api_key
        # self._current_usage = self._get_api_usage()['usage']

    def get_exchange_rates(self, currency_pairs) -> Dict[Tuple[str, str], float]:
        pair_rates = [self._get_exchange_rate(pair) for pair in currency_pairs]
        return {(x['fr'],x['to']):x['val'] for x in pair_rates if x is not None}

    def _get_exchange_rate(self, currency_pair) -> ExchangeRate:
        combined_rate = '_'.join(currency_pair)
        request_params = {'q':combined_rate, 'apiKey':self.api_key}
        response = requests.get(self.url_base + self.convert_endpoint, params=request_params)
        if response.status_code == 200:
            rate_response = ExchangeRateResponse(**json.loads(response.text))
            if not rate_response.results:
                return #No exchange rate available
            return rate_response.results[combined_rate]

    def _get_api_usage(self) -> ExchangeRateUsageResponse:
        request_params = {'apiKey':self.api_key}
        response = requests.get(self.url_base + self.usage_endpoint, params=request_params)
        if response.status_code == 200:
            return ExchangeRateUsageResponse(**json.loads(response.text))