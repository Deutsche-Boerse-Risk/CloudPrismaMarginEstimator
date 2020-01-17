"""
The following example generates a portfolio in CSV format.
The portfolio has a position in Euro-Bund futures.
Initial margin is calculated and results printed.

Remember to replace os.environ['KEY'] in api_header with your own API-key

To register for an API-key please visit

https://console.developer.deutsche-boerse.com/apis
"""

import requests
import json
import os

url_base = ("https://api.developer.deutsche-boerse.com/prod/prisma-margin-estimator-2-0/2.0.0/")
api_header = {"X-DBP-APIKEY": os.environ['KEY'] }

series = requests.get(url_base + "series",
                 params = {'products': 'FGBL'},
                 headers = api_header).json()

etd = {'line_no': 1, 'iid': series['list_series'][-1]['iid'], 'net_ls_balance': -500}

results = requests.post(url_base + 'estimator', 
                        headers = api_header,
                           json = {'portfolio_components':[
                                       {'type': 'etd_portfolio', 'etd_portfolio': [etd]},
                                   ],
                                   'clearing_currency': 'EUR'}
                        ).json()
print('Example of margin output:')
print(json.dumps(results['portfolio_margin'], indent=4, sort_keys=True))
