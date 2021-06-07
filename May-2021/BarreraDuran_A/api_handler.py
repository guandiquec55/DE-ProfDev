import requests
import json
import more_itertools


def get_latest_rate(from_to_list, key='86c11fb2002736345d0d'):
    """ 
    Returns the latest currency rate exchanges between two currencies given a list of
    currencies to compare where USD_MXN is a "value" in the list in dict format

    Parameters
    ----------
    server: `list[string]`
        a list of currency exchange rates to get
    key: `string`
        the api token that can be used to authenticate and get a response from the API with

    Returns
    -------
    output_dic : `dict`
        a dictionary of currency exchange rates in current time
    """
    output_dict = {}
    tmp_list = from_to_list.split(',')
    for chunk in more_itertools.chunked(tmp_list, 2):
        two_rates = ','.join(chunk)
        req = f'https://free.currconv.com/api/v7/convert?q={two_rates}&compact=ultra&apiKey={key}'
        r = requests.get(req)
        response = json.loads(r.text)
        output_dict.update(response)
    return output_dict
