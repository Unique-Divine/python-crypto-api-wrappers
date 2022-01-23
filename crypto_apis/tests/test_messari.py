import crypto_apis
import pandas as pd
from typing import List

#%%  Price data 

from crypto_apis.messari import messari_api

def prices_test_query():
    assets = ['btc', 'eth']
    metric = "price"
    start = "2020-06-01"
    end = "2020-07-01"
    prices_df = messari_api.get_metric_timeseries(
        asset_slugs=assets, asset_metric=metric, start=start, end=end)
    breakpoint()
    
# prices_test_query() # It works. Now, we just need parameters.


